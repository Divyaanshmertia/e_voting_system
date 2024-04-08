from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_login import LoginManager, login_required
from google.cloud import storage
from flask import Flask, render_template, redirect, url_for, request  # Import 'request' here
from flask import jsonify
from google.cloud import storage

import requests
# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()



def create_app():
    app = Flask(__name__)
    CORS(app)

    # Configure your Flask app
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Divyaansh%40IITJ@34.136.108.197/app'
    app.config['GCS_BUCKET'] = 'facerepo'
    app.config['SECRET_KEY'] = 'your_very_secret_key_here'

    # Initialize SQLAlchemy and Migrate with the app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Set the login route for flask-login
    login_manager.login_view = 'user_blueprint.login'

    # Import models here to avoid circular imports
    from app.models import Vote, User, Candidate

    # Import and register your blueprints
    from app.views.users import user_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/api/users')

    from app.views.dashboard import dashboard_blueprint
    app.register_blueprint(dashboard_blueprint, url_prefix='/dashboard')

    from app.views.candidates import candidate_blueprint
    app.register_blueprint(candidate_blueprint, url_prefix='/api/candidates')

    from app.views.user_images import user_image_blueprint
    app.register_blueprint(user_image_blueprint, url_prefix='/api/user_images')

    from app.views.votes import vote_blueprint
    app.register_blueprint(vote_blueprint, url_prefix='/vote')

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Define your Flask app routes here
    @app.route('/login')
    def index():
        return redirect(url_for('user_blueprint.login'))

    @app.route('/dashboard')
    @login_required
    def dashboard():
        total_votes = Vote.query.count()
        total_voters = User.query.count()
        candidates = Candidate.query.all()
        vote_counts = {candidate.id: Vote.query.filter_by(candidate_id=candidate.id).count() for candidate in candidates}
        print("Total Votes:", total_votes, "Total Voters:", total_voters)
        return render_template('dashboard.html', total_votes=total_votes, total_voters=total_voters, candidates=candidates, vote_counts=vote_counts)

    @app.route('/votes')
    @login_required
    def votes():
        return redirect(url_for('vote_blueprint.vote'))

    @app.route('/profile')
    @login_required
    def profile():
        return render_template('profile.html')

    from flask_login import current_user

    @app.route('/facial-recognition')
    @login_required
    def facial_recognition():
        username = current_user.voter_id  # Assuming 'username' is the attribute for the user's username
        return render_template('facial.html', username=username)

    @app.route('/api/users/<username>/images')
    def get_user_images(username):
        # Verify that the requested username matches the logged-in user to prevent unauthorized access
        client = storage.Client()
        bucket = client.bucket(app.config['GCS_BUCKET'])
        prefix = f'{username}/'
        blobs = bucket.list_blobs(prefix=prefix)
        image_urls = [blob.public_url for blob in blobs if blob.name.lower().endswith(('.png', '.jpg', '.jpeg'))]
        print(image_urls)
        return jsonify({'images': image_urls})

    @app.route('/upload', methods=['POST'])
    def upload_file():
        username = request.form['username']  # Retrieve username from form data
        file = request.files.get('file')
        if not file or file.filename == '':
            return redirect(request.url)
        else:
            client = storage.Client()
            bucket = client.bucket(app.config['GCS_BUCKET'])
            # Include the username in the blob path
            blob_path = f"{username}/{file.filename}"
            blob = bucket.blob(blob_path)
            blob.upload_from_string(
                file.read(),
                content_type=file.content_type
            )
            return 'File uploaded successfully', 200

    @app.route('/upload-form')
    def show_upload_form():
        return render_template('upload_form.html')

    return app
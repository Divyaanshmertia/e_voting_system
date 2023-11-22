from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from google.cloud import storage
from flask_cors import CORS

db = SQLAlchemy()
migrate = None

def create_app():
    app = Flask(__name__)
    CORS(app)
    # Configure your Flask app
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:divyaansh@34.31.96.18/app'
    app.config['GCS_BUCKET'] = 'divyaansh'
    # Initialize SQLAlchemy and Migrate with the app
    db.init_app(app)
    global migrate
    migrate = Migrate(app, db)

    @app.route('/facial-recognition')
    def facial_recognition():
        return render_template('facial.html')
    # Import and register your blueprints
    from app.views.users import user_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/api')

    from app.views.candidates import candidate_blueprint
    app.register_blueprint(candidate_blueprint, url_prefix='/api')

    from app.views.votes import vote_blueprint
    app.register_blueprint(vote_blueprint, url_prefix='/api')

    from app.views.user_images import user_image_blueprint
    app.register_blueprint(user_image_blueprint, url_prefix='/api')

    return app

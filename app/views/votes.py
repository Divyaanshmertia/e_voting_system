from flask import Blueprint, request, jsonify
from app import db
from app.models import Vote
from sqlalchemy.exc import SQLAlchemyError

vote_blueprint = Blueprint('vote_blueprint', __name__)

# votes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Candidate, Vote
# Add other necessary imports

vote_blueprint = Blueprint('vote_blueprint', __name__)

@vote_blueprint.route('/vote', methods=['GET', 'POST'])
@login_required
def vote():
    if request.method == 'POST':
        candidate_id = request.form.get('vote')
        # Implement additional checks if necessary, e.g., if user has already voted

        new_vote = Vote(user_id=current_user.id, candidate_id=candidate_id)
        db.session.add(new_vote)
        db.session.commit()
        flash('Your vote has been cast!', 'success')
        return redirect(url_for('dashboard_blueprint.dashboard'))

    candidates = Candidate.query.all()
    return render_template('vote.html', candidates=candidates)

# Register the blueprint in your main application (__init__.py or app.py)
# from app.views.votes import vote_blueprint
# app.register_blueprint(vote_blueprint, url_prefix='/votes')

@vote_blueprint.route('/votes', methods=['GET'])
def get_votes():
    try:
        votes = Vote.query.all()
        return jsonify([vote.to_dict() for vote in votes]), 200
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500



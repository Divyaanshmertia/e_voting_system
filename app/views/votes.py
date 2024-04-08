from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Candidate, Vote

vote_blueprint = Blueprint('vote_blueprint', __name__)

@vote_blueprint.route('/vote', methods=['GET', 'POST'])
@login_required
def vote():
    if request.method == 'POST':
        candidate_id = request.form.get('vote')
        existing_vote = Vote.query.filter_by(user_id=current_user.id).first()

        if existing_vote:
            flash('You have already voted!', 'warning')
            return redirect(url_for('dashboard_blueprint.dashboard'))

        try:
            new_vote = Vote(user_id=current_user.id, candidate_id=candidate_id)
            db.session.add(new_vote)
            db.session.commit()
            flash('Your vote has been cast!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error recording your vote. Please try again.', 'danger')
            print(e)  # For debugging purposes

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



from flask import Blueprint, request, jsonify
from app import db
from app.models import Vote
from sqlalchemy.exc import SQLAlchemyError

vote_blueprint = Blueprint('vote_blueprint', __name__)

@vote_blueprint.route('/votes', methods=['POST'])
def cast_vote():
    data = request.json
    new_vote = Vote(
        user_id=data.get('user_id'),
        candidate_id=data.get('candidate_id')
    )
    try:
        db.session.add(new_vote)
        db.session.commit()
        return jsonify({"message": "Vote cast successfully"}), 201
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500

@vote_blueprint.route('/votes', methods=['GET'])
def get_votes():
    try:
        votes = Vote.query.all()
        return jsonify([vote.to_dict() for vote in votes]), 200
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500



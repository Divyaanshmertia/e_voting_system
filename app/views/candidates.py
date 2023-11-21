from flask import Blueprint, request, jsonify
from app import db
from app.models import Candidate
from sqlalchemy.exc import SQLAlchemyError

candidate_blueprint = Blueprint('candidate_blueprint', __name__)

@candidate_blueprint.route('/candidates', methods=['GET'])
def get_candidates():
    try:
        candidates = Candidate.query.all()
        return jsonify([candidate.to_dict() for candidate in candidates]), 200
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500

@candidate_blueprint.route('/candidate/<int:candidate_id>', methods=['GET'])
def get_candidate(candidate_id):
    try:
        candidate = Candidate.query.get(candidate_id)
        if candidate:
            return jsonify(candidate.to_dict()), 200
        return jsonify({"message": "Candidate not found"}), 404
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500

@candidate_blueprint.route('/candidate', methods=['POST'])
def create_candidate():
    data = request.json
    new_candidate = Candidate(
        name=data.get('name'),
        party=data.get('party'),
        constituency=data.get('constituency')
    )
    try:
        db.session.add(new_candidate)
        db.session.commit()
        return jsonify(new_candidate.to_dict()), 201
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500

@candidate_blueprint.route('/candidate/<int:candidate_id>', methods=['PUT'])
def update_candidate(candidate_id):
    candidate = Candidate.query.get(candidate_id)
    if not candidate:
        return jsonify({"message": "Candidate not found"}), 404

    data = request.json
    try:
        candidate.name = data.get('name', candidate.name)
        candidate.party = data.get('party', candidate.party)
        candidate.constituency = data.get('constituency', candidate.constituency)
        db.session.commit()
        return jsonify(candidate.to_dict()), 200
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500

@candidate_blueprint.route('/candidate/<int:candidate_id>', methods=['DELETE'])
def delete_candidate(candidate_id):
    candidate = Candidate.query.get(candidate_id)
    if not candidate:
        return jsonify({"message": "Candidate not found"}), 404
    try:
        db.session.delete(candidate)
        db.session.commit()
        return jsonify({"message": "Candidate deleted"}), 200
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500




from flask import Blueprint, request, jsonify
from app import db
from app.models.User import User
from sqlalchemy.exc import SQLAlchemyError

user_blueprint = Blueprint('user_blueprint', __name__)

@user_blueprint.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        return jsonify([user.to_dict() for user in users]), 200
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500

@user_blueprint.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = User.query.get(user_id)
        if user:
            return jsonify(user.to_dict()), 200
        return jsonify({"message": "User not found"}), 404
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500

@user_blueprint.route('/user', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(
        voter_id=data.get('voter_id'),
        name=data.get('name'),
        email=data.get('email'),
        constituency=data.get('constituency')
    )
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_dict()), 201
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500

@user_blueprint.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.json
    try:
        user.voter_id = data.get('voter_id', user.voter_id)
        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)
        user.constituency = data.get('constituency', user.constituency)
        db.session.commit()
        return jsonify(user.to_dict()), 200
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500

@user_blueprint.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted"}), 200
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500


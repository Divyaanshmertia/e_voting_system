from flask import Blueprint, request, jsonify
from app import db
from app.models import UserImage
from sqlalchemy.exc import SQLAlchemyError

user_image_blueprint = Blueprint('user_image_blueprint', __name__)

@user_image_blueprint.route('/user_images', methods=['POST'])
def add_user_image():
    data = request.json
    new_image = UserImage(
        user_id=data.get('user_id'),
        image_url=data.get('image_url')
    )
    try:
        db.session.add(new_image)
        db.session.commit()
        return jsonify(new_image.to_dict()), 201
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500

@user_image_blueprint.route('/user_images/<int:user_id>', methods=['GET'])
def get_user_images(user_id):
    try:
        images = UserImage.query.filter_by(user_id=user_id).all()
        return jsonify([image.to_dict() for image in images]), 200
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500



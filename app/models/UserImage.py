# in app/models/user_image.py
from app import db


class UserImage(db.Model):
    __tablename__ = 'user_images'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)  # URL to the image

    def __repr__(self):
        return f'<UserImage {self.image_url}>'

    # This function converts the UserImage object to a dictionary
    def user_image_to_dict(user_image):
        return {
            'id': user_image.id,
            'user_id': user_image.user_id,
            'image_url': user_image.image_url
        }

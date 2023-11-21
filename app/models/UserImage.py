# in app/models/user_image.py
from app import db


class UserImage(db.Model):
    __tablename__ = 'user_images'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)  # URL to the image

    def __repr__(self):
        return f'<UserImage {self.image_url}>'

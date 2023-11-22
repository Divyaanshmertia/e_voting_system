from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .. import login_manager
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    voter_id = db.Column(db.String(10), unique=True, nullable=False)  # Unique Voter ID
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    constituency = db.Column(db.String(100))  # Constituency of the voter
    # Relationships
    votes = db.relationship('Vote', backref='voter', lazy='dynamic')
    images = db.relationship('UserImage', backref='user', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.name}>'


    def to_dict(self):
        return {
            'id': self.id,
            'voter_id': self.voter_id,
            'name': self.name,
            'email': self.email,
            'constituency': self.constituency,
            'password_hash' : self.password_hash
        }

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Flask-Login integration
    def get_id(self):
        return self.id


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

    


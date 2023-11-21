from app import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    voter_id = db.Column(db.String(10), unique=True, nullable=False)  # Unique Voter ID
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
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
            'constituency': self.constituency
        }

    


# in app/models/candidate.py
from app import db

class Candidate(db.Model):
    __tablename__ = 'candidates'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    party = db.Column(db.String(100))  # Political party
    constituency = db.Column(db.String(100))  # Constituency

    # Relationship
    votes = db.relationship('Vote', backref='candidate', lazy='dynamic')

    def __repr__(self):
        return f'<Candidate {self.name}>'

    def candidate_to_dict(candidate):
        return {
            'id': candidate.id,
            'name': candidate.name,
            'party': candidate.party,
            'constituency': candidate.constituency
        }

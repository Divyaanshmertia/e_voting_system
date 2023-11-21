# in app/models/vote.py
from app import db
from datetime import datetime

class Vote(db.Model):
    __tablename__ = 'votes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Vote {self.user_id} for {self.candidate_id}>'

    # This function converts the Vote object to a dictionary
    def vote_to_dict(vote):
        return {
            'id': vote.id,
            'user_id': vote.user_id,
            'candidate_id': vote.candidate_id,
            'timestamp': vote.timestamp.isoformat()
        }

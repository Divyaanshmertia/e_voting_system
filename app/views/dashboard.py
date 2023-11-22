# In your views file
from flask import Blueprint, render_template
from flask_login import login_required

from app.models import Candidate, Vote

dashboard_blueprint = Blueprint('dashboard_blueprint', __name__)

@dashboard_blueprint.route('/dashboard')
@login_required
def dashboard():
    candidates = Candidate.query.all()
    vote_counts = {candidate.id: Vote.query.filter_by(candidate_id=candidate.id).count() for candidate in candidates}
    return render_template('dashboard.html', vote_counts=vote_counts, candidates=candidates)

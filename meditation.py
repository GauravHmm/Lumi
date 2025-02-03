from flask import Blueprint, request, jsonify
from models import MeditationLog, DailyRoutine
from database import db
from services.gemini_service import get_meditation_suggestions

meditation_bp = Blueprint('meditation', __name__)

@meditation_bp.route('/api/meditation-log', methods=['POST'])
def log_meditation():
    data = request.json
    new_log = MeditationLog(user_id=data['user_id'], duration=data['duration'], type=data['type'])
    db.session.add(new_log)
    db.session.commit()
    return jsonify({'message': 'Meditation logged successfully', 'log_id': new_log.id}), 201

@meditation_bp.route('/api/meditation-suggestions', methods=['GET'])
def get_suggestions():
    user_id = request.args.get('user_id')
    # Fetch user's recent routines and meditation logs
    recent_routines = DailyRoutine.query.filter_by(user_id=user_id).order_by(DailyRoutine.date.desc()).limit(5).all()
    recent_logs = MeditationLog.query.filter_by(user_id=user_id).order_by(MeditationLog.date.desc()).limit(5).all()

    # Use Gemini API to get personalized suggestions
    suggestions = get_meditation_suggestions(recent_routines, recent_logs)
    return jsonify(suggestions)


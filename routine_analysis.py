from flask import Blueprint, request, jsonify
from models import DailyRoutine
from database import db
from services.gemini_service import analyze_routine

routine_analysis_bp = Blueprint('routine_analysis', __name__)

@routine_analysis_bp.route('/api/routine-analysis', methods=['POST'])
def analyze_daily_routine():
    data = request.json
    routine_data = data['routine_data']
    user_id = data['user_id']

    # Use Gemini API to analyze the routine
    analysis = analyze_routine(routine_data)

    # Save routine and analysis to database
    new_routine = DailyRoutine(user_id=user_id, data=routine_data, analysis=analysis)
    db.session.add(new_routine)
    db.session.commit()

    return jsonify({'analysis': analysis})

@routine_analysis_bp.route('/api/routine-history', methods=['GET'])
def get_routine_history():
    user_id = request.args.get('user_id')
    routines = DailyRoutine.query.filter_by(user_id=user_id).order_by(DailyRoutine.date.desc()).all()
    return jsonify([{'id': r.id, 'date': r.date, 'data': r.data, 'analysis': r.analysis} for r in routines])


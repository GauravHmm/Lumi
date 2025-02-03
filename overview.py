from flask import Blueprint, jsonify
from models import DailyRoutine, Goal, MeditationLog
from database import db
from datetime import datetime, timedelta
from services.rag_service import get_rag_insights

overview_bp = Blueprint('overview', __name__)

@overview_bp.route('/api/overview', methods=['GET'])
def get_overview():
    # Fetch data for the past week and month
    end_date = datetime.now()
    start_date_week = end_date - timedelta(days=7)
    start_date_month = end_date - timedelta(days=30)

    # Fetch data from database
    weekly_routines = DailyRoutine.query.filter(DailyRoutine.date >= start_date_week).all()
    monthly_routines = DailyRoutine.query.filter(DailyRoutine.date >= start_date_month).all()
    goals = Goal.query.filter(Goal.target_date >= start_date_month).all()
    meditation_logs = MeditationLog.query.filter(MeditationLog.date >= start_date_month).all()

    # Use RAG to generate insights
    weekly_insights = get_rag_insights(weekly_routines)
    monthly_insights = get_rag_insights(monthly_routines)

    # Prepare response data
    response = {
        'weekly_overview': weekly_insights,
        'monthly_overview': monthly_insights,
        'goals_progress': [{'id': g.id, 'title': g.title, 'completed': g.completed} for g in goals],
        'meditation_stats': {
            'total_sessions': len(meditation_logs),
            'total_minutes': sum(log.duration for log in meditation_logs)
        }
    }

    return jsonify(response)


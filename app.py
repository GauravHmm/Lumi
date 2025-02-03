from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from datetime import datetime, timedelta
import google.generativeai as genai

# Create Flask app
app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3306/lumi_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with the app
db = SQLAlchemy(app)

# Retrieve API key from environment variable
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
else:
    raise ValueError("API key is not set. Please set GEMINI_API_KEY in your environment variables.")

# Import models
from models import User, DailyRoutine, Goal, MeditationLog, CommunityPost

# Import services
from services.gemini_service import analyze_routine, get_meditation_suggestions
from services.rag_service import get_rag_insights

# Create tables
with app.app_context():
    db.create_all()

# API Routes
@app.route('/api/overview', methods=['GET'])
def get_overview():
    end_date = datetime.now()
    start_date_week = end_date - timedelta(days=7)
    start_date_month = end_date - timedelta(days=30)

    weekly_routines = DailyRoutine.query.filter(DailyRoutine.date >= start_date_week).all()
    monthly_routines = DailyRoutine.query.filter(DailyRoutine.date >= start_date_month).all()
    goals = Goal.query.filter(Goal.target_date >= start_date_month).all()
    meditation_logs = MeditationLog.query.filter(MeditationLog.date >= start_date_month).all()

    weekly_insights = get_rag_insights(weekly_routines)
    monthly_insights = get_rag_insights(monthly_routines)

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

@app.route('/api/goals', methods=['GET', 'POST'])
def handle_goals():
    if request.method == 'GET':
        goals = Goal.query.all()
        return jsonify([{'id': g.id, 'title': g.title, 'description': g.description, 'target_date': g.target_date, 'completed': g.completed} for g in goals])
    elif request.method == 'POST':
        data = request.json
        new_goal = Goal(user_id=data['user_id'], title=data['title'], description=data['description'], target_date=data['target_date'])
        db.session.add(new_goal)
        db.session.commit()
        return jsonify({'message': 'Goal created successfully', 'goal_id': new_goal.id}), 201

@app.route('/api/goals/<int:goal_id>', methods=['PUT', 'DELETE'])
def handle_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    if request.method == 'PUT':
        data = request.json
        goal.title = data.get('title', goal.title)
        goal.description = data.get('description', goal.description)
        goal.target_date = data.get('target_date', goal.target_date)
        goal.completed = data.get('completed', goal.completed)
        db.session.commit()
        return jsonify({'message': 'Goal updated successfully'})
    elif request.method == 'DELETE':
        db.session.delete(goal)
        db.session.commit()
        return jsonify({'message': 'Goal deleted successfully'})

@app.route('/api/routine-analysis', methods=['POST'])
def analyze_daily_routine():
    data = request.json
    routine_data = data['routine_data']
    user_id = data['user_id']

    analysis = analyze_routine(routine_data)

    new_routine = DailyRoutine(user_id=user_id, data=routine_data, analysis=analysis)
    db.session.add(new_routine)
    db.session.commit()

    return jsonify({'analysis': analysis})

@app.route('/api/routine-history', methods=['GET'])
def get_routine_history():
    user_id = request.args.get('user_id')
    routines = DailyRoutine.query.filter_by(user_id=user_id).order_by(DailyRoutine.date.desc()).all()
    return jsonify([{'id': r.id, 'date': r.date, 'data': r.data, 'analysis': r.analysis} for r in routines])

@app.route('/api/meditation-log', methods=['POST'])
def log_meditation():
    data = request.json
    new_log = MeditationLog(user_id=data['user_id'], duration=data['duration'], type=data['type'])
    db.session.add(new_log)
    db.session.commit()
    return jsonify({'message': 'Meditation logged successfully', 'log_id': new_log.id}), 201

@app.route('/api/meditation-suggestions', methods=['GET'])
def get_suggestions():
    user_id = request.args.get('user_id')
    recent_routines = DailyRoutine.query.filter_by(user_id=user_id).order_by(DailyRoutine.date.desc()).limit(5).all()
    recent_logs = MeditationLog.query.filter_by(user_id=user_id).order_by(MeditationLog.date.desc()).limit(5).all()

    suggestions = get_meditation_suggestions(recent_routines, recent_logs)
    return jsonify(suggestions)

@app.route('/api/community-posts', methods=['GET', 'POST'])
def handle_community_posts():
    if request.method == 'GET':
        posts = CommunityPost.query.order_by(CommunityPost.timestamp.desc()).all()
        return jsonify([{'id': p.id, 'user_id': p.user_id, 'content': p.content, 'timestamp': p.timestamp} for p in posts])
    elif request.method == 'POST':
        data = request.json
        new_post = CommunityPost(user_id=data['user_id'], content=data['content'])
        db.session.add(new_post)
        db.session.commit()
        return jsonify({'message': 'Post created successfully', 'post_id': new_post.id}), 201

@app.route('/api/community-posts/<int:post_id>', methods=['DELETE'])
def delete_community_post(post_id):
    post = CommunityPost.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Post deleted successfully'})

# HTML Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/overview')
def overview():
    return render_template('overview.html')

@app.route('/goals')
def goals():
    return render_template('goals.html')

@app.route('/routine-analysis')
def routine_analysis():
    return render_template('routine_analysis.html')

@app.route('/meditation')
def meditation():
    return render_template('meditation.html')

@app.route('/community')
def community():
    return render_template('community.html')

if __name__ == '__main__':
    app.run(debug=True)


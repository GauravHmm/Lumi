from flask import Blueprint, request, jsonify
from models import Goal
from database import db

goals_bp = Blueprint('goals', __name__)

@goals_bp.route('/api/goals', methods=['GET', 'POST'])
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

@goals_bp.route('/api/goals/<int:goal_id>', methods=['PUT', 'DELETE'])
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


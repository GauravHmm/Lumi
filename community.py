from flask import Blueprint, request, jsonify
from models import CommunityPost
from database import db

community_bp = Blueprint('community', __name__)

@community_bp.route('/api/community-posts', methods=['GET', 'POST'])
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

@community_bp.route('/api/community-posts/<int:post_id>', methods=['DELETE'])
def delete_community_post(post_id):
    post = CommunityPost.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Post deleted successfully'})


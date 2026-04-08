"""Favorites routes"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import get_db

favorites_bp = Blueprint('favorites', __name__)

@favorites_bp.route('/', methods=['GET'])
@jwt_required()
def get_favorites():
    user_id = get_jwt_identity()
    db = get_db()
    rows = db.execute('''
        SELECT p.*, f.id as fav_id FROM favorites f
        JOIN properties p ON f.property_id = p.id
        WHERE f.user_id = ?
        ORDER BY f.created_at DESC
    ''', (user_id,)).fetchall()
    import json
    result = []
    for r in rows:
        d = dict(r)
        d['images'] = json.loads(d['images']) if d['images'] else []
        d['amenities'] = json.loads(d['amenities']) if d['amenities'] else []
        d['is_favorited'] = True
        result.append(d)
    return jsonify({'favorites': result})

@favorites_bp.route('/', methods=['POST'])
@jwt_required()
def add_favorite():
    user_id = get_jwt_identity()
    data = request.get_json()
    property_id = data.get('property_id')
    if not property_id:
        return jsonify({'error': 'property_id required'}), 400
    db = get_db()
    existing = db.execute(
        'SELECT id FROM favorites WHERE user_id = ? AND property_id = ?',
        (user_id, property_id)
    ).fetchone()
    if existing:
        return jsonify({'message': 'Already in favorites'}), 200
    db.execute('INSERT INTO favorites (user_id, property_id) VALUES (?, ?)', (user_id, property_id))
    db.commit()
    return jsonify({'message': 'Added to favorites'}), 201

@favorites_bp.route('/<int:property_id>', methods=['DELETE'])
@jwt_required()
def remove_favorite(property_id):
    user_id = get_jwt_identity()
    db = get_db()
    db.execute('DELETE FROM favorites WHERE user_id = ? AND property_id = ?', (user_id, property_id))
    db.commit()
    return jsonify({'message': 'Removed from favorites'})

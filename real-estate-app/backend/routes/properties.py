"""Properties routes — CRUD with filtering and pagination"""
import json
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from database import get_db

properties_bp = Blueprint('properties', __name__)

def serialize_property(row, favorited_ids=None):
    d = dict(row)
    d['images'] = json.loads(d['images']) if d['images'] else []
    d['amenities'] = json.loads(d['amenities']) if d['amenities'] else []
    if favorited_ids is not None:
        d['is_favorited'] = d['id'] in favorited_ids
    else:
        d['is_favorited'] = False
    return d

def get_favorited_ids(user_id, db):
    if not user_id:
        return set()
    rows = db.execute('SELECT property_id FROM favorites WHERE user_id = ?', (user_id,)).fetchall()
    return {r['property_id'] for r in rows}

@properties_bp.route('/', methods=['GET'])
def list_properties():
    # Try to get auth user for wishlist state
    user_id = None
    try:
        verify_jwt_in_request(optional=True)
        user_id = get_jwt_identity()
    except Exception:
        pass

    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 12))
    city = request.args.get('city', '').strip()
    location = request.args.get('location', '').strip()
    min_price = request.args.get('min_price', type=int)
    max_price = request.args.get('max_price', type=int)
    bhk = request.args.get('bhk', type=int)
    prop_type = request.args.get('type', '').strip()
    furnishing = request.args.get('furnishing', '').strip()
    sort = request.args.get('sort', 'newest')

    query = 'SELECT * FROM properties WHERE 1=1'
    params = []

    if city:
        query += ' AND LOWER(city) LIKE ?'
        params.append(f'%{city.lower()}%')
    if location:
        query += ' AND (LOWER(location) LIKE ? OR LOWER(city) LIKE ?)'
        params.extend([f'%{location.lower()}%', f'%{location.lower()}%'])
    if min_price is not None:
        query += ' AND price >= ?'
        params.append(min_price)
    if max_price is not None:
        query += ' AND price <= ?'
        params.append(max_price)
    if bhk is not None:
        query += ' AND bhk = ?'
        params.append(bhk)
    if prop_type:
        query += ' AND LOWER(type) = ?'
        params.append(prop_type.lower())
    if furnishing:
        query += ' AND LOWER(furnishing) = ?'
        params.append(furnishing.lower())

    # Sort
    if sort == 'price_asc':
        query += ' ORDER BY price ASC'
    elif sort == 'price_desc':
        query += ' ORDER BY price DESC'
    elif sort == 'area_asc':
        query += ' ORDER BY area_sqft ASC'
    else:  # newest
        query += ' ORDER BY created_at DESC'

    db = get_db()
    all_rows = db.execute(query, params).fetchall()
    total = len(all_rows)
    offset = (page - 1) * per_page
    rows = all_rows[offset:offset + per_page]

    favorited_ids = get_favorited_ids(user_id, db)
    properties = [serialize_property(r, favorited_ids) for r in rows]

    return jsonify({
        'properties': properties,
        'total': total,
        'page': page,
        'per_page': per_page,
        'total_pages': (total + per_page - 1) // per_page
    })

@properties_bp.route('/<int:prop_id>', methods=['GET'])
def get_property(prop_id):
    user_id = None
    try:
        verify_jwt_in_request(optional=True)
        user_id = get_jwt_identity()
    except Exception:
        pass

    db = get_db()
    row = db.execute('SELECT * FROM properties WHERE id = ?', (prop_id,)).fetchone()
    if not row:
        return jsonify({'error': 'Property not found'}), 404

    favorited_ids = get_favorited_ids(user_id, db)
    return jsonify(serialize_property(row, favorited_ids))

@properties_bp.route('/', methods=['POST'])
@jwt_required()
def create_property():
    user_id = get_jwt_identity()
    db = get_db()
    user = db.execute('SELECT role FROM users WHERE id = ?', (user_id,)).fetchone()
    if not user or user['role'] != 'admin':
        return jsonify({'error': 'Admin access required'}), 403

    data = request.get_json()
    required = ['title', 'price', 'location', 'city', 'type']
    for f in required:
        if not data.get(f):
            return jsonify({'error': f'{f} is required'}), 400

    amenities = json.dumps(data.get('amenities', []))
    images = json.dumps(data.get('images', []))

    cursor = db.execute('''
        INSERT INTO properties
        (title, price, location, city, bhk, type, furnishing, area_sqft,
         description, amenities, images, lat, lng, owner_contact)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['title'], int(data['price']), data['location'], data['city'],
        int(data.get('bhk', 0)), data['type'], data.get('furnishing', 'Unfurnished'),
        int(data.get('area_sqft', 0)), data.get('description', ''),
        amenities, images, float(data.get('lat', 0)), float(data.get('lng', 0)),
        data.get('owner_contact', '')
    ))
    db.commit()

    row = db.execute('SELECT * FROM properties WHERE id = ?', (cursor.lastrowid,)).fetchone()
    return jsonify(serialize_property(row)), 201

@properties_bp.route('/<int:prop_id>', methods=['PUT'])
@jwt_required()
def update_property(prop_id):
    user_id = get_jwt_identity()
    db = get_db()
    user = db.execute('SELECT role FROM users WHERE id = ?', (user_id,)).fetchone()
    if not user or user['role'] != 'admin':
        return jsonify({'error': 'Admin access required'}), 403

    data = request.get_json()
    existing = db.execute('SELECT * FROM properties WHERE id = ?', (prop_id,)).fetchone()
    if not existing:
        return jsonify({'error': 'Property not found'}), 404

    amenities = json.dumps(data.get('amenities', json.loads(existing['amenities'])))
    images_raw = data.get('images', json.loads(existing['images']))
    if isinstance(images_raw, str):
        try:
            images_raw = json.loads(images_raw)
        except Exception:
            images_raw = [images_raw]
    images = json.dumps(images_raw)

    db.execute('''
        UPDATE properties SET
        title=?, price=?, location=?, city=?, bhk=?, type=?, furnishing=?,
        area_sqft=?, description=?, amenities=?, images=?, lat=?, lng=?, owner_contact=?
        WHERE id=?
    ''', (
        data.get('title', existing['title']),
        int(data.get('price', existing['price'])),
        data.get('location', existing['location']),
        data.get('city', existing['city']),
        int(data.get('bhk', existing['bhk'])),
        data.get('type', existing['type']),
        data.get('furnishing', existing['furnishing']),
        int(data.get('area_sqft', existing['area_sqft'])),
        data.get('description', existing['description']),
        amenities, images,
        float(data.get('lat', existing['lat'])),
        float(data.get('lng', existing['lng'])),
        data.get('owner_contact', existing['owner_contact']),
        prop_id
    ))
    db.commit()
    row = db.execute('SELECT * FROM properties WHERE id = ?', (prop_id,)).fetchone()
    return jsonify(serialize_property(row))

@properties_bp.route('/<int:prop_id>', methods=['DELETE'])
@jwt_required()
def delete_property(prop_id):
    user_id = get_jwt_identity()
    db = get_db()
    user = db.execute('SELECT role FROM users WHERE id = ?', (user_id,)).fetchone()
    if not user or user['role'] != 'admin':
        return jsonify({'error': 'Admin access required'}), 403

    existing = db.execute('SELECT id FROM properties WHERE id = ?', (prop_id,)).fetchone()
    if not existing:
        return jsonify({'error': 'Property not found'}), 404

    db.execute('DELETE FROM favorites WHERE property_id = ?', (prop_id,))
    db.execute('DELETE FROM properties WHERE id = ?', (prop_id,))
    db.commit()
    return jsonify({'message': 'Property deleted'})

@properties_bp.route('/cities', methods=['GET'])
def list_cities():
    db = get_db()
    rows = db.execute('SELECT DISTINCT city FROM properties ORDER BY city').fetchall()
    return jsonify({'cities': [r['city'] for r in rows]})

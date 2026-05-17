from flask import Blueprint, jsonify, request
from models.menu_item import MenuItem
from extensions import db

menu_bp = Blueprint('menu', __name__)

@menu_bp.route('/menu', methods=['GET'])
def get_all_menu_items():
    """Get all menu items"""
    try:
        items = MenuItem.query.filter_by(is_available=True).all()
        return jsonify({
            'success': True,
            'data': [item.to_dict() for item in items]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@menu_bp.route('/menu/<category>', methods=['GET'])
def get_menu_by_category(category):
    """Get menu items by category"""
    try:
        items = MenuItem.query.filter_by(category=category, is_available=True).all()
        return jsonify({
            'success': True,
            'data': [item.to_dict() for item in items]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@menu_bp.route('/menu/item/<int:item_id>', methods=['GET'])
def get_menu_item(item_id):
    """Get single menu item by ID"""
    try:
        item = MenuItem.query.get_or_404(item_id)
        return jsonify({
            'success': True,
            'data': item.to_dict()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@menu_bp.route('/menu', methods=['POST'])
def create_menu_item():
    """Create new menu item (admin only)"""
    try:
        data = request.get_json()
        
        item = MenuItem(
            name=data['name'],
            description=data.get('description'),
            price=data['price'],
            category=data['category'],
            image_url=data.get('image_url'),
            tag=data.get('tag')
        )
        
        db.session.add(item)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': item.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@menu_bp.route('/menu/item/<int:item_id>', methods=['PUT'])
def update_menu_item(item_id):
    """Update menu item (admin only)"""
    try:
        item = MenuItem.query.get_or_404(item_id)
        data = request.get_json()
        
        for key, value in data.items():
            if hasattr(item, key):
                setattr(item, key, value)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': item.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@menu_bp.route('/menu/item/<int:item_id>', methods=['DELETE'])
def delete_menu_item(item_id):
    """Delete menu item (admin only)"""
    try:
        item = MenuItem.query.get_or_404(item_id)
        item.is_available = False  # Soft delete
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Menu item deleted successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
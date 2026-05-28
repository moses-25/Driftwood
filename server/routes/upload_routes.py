"""
Upload routes
Handles all file upload API endpoints
"""
from flask import Blueprint, jsonify, request, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.file_service import FileService
from models.product import Product
from models.category import Category
from extensions import db
from utils.decorators import admin_required, staff_required
from config import Config
import logging
import os

upload_bp = Blueprint('upload', __name__)
logger = logging.getLogger(__name__)


@upload_bp.route('/uploads/<path:filename>', methods=['GET'])
def serve_file(filename):
    """
    Serve uploaded file
    
    Path Parameters:
        filename (str): File path (e.g., products/image.jpg)
        
    Returns:
        200: File content
        404: File not found
    """
    try:
        upload_folder = Config.UPLOAD_FOLDER
        file_path = os.path.join(upload_folder, filename)
        
        if not os.path.exists(file_path):
            return jsonify({'success': False, 'error': 'File not found'}), 404
        
        # Get directory and filename
        directory = os.path.dirname(file_path)
        file_name = os.path.basename(file_path)
        
        return send_from_directory(directory, file_name)
        
    except Exception as e:
        logger.error(f"Error serving file: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@upload_bp.route('/upload/product-image', methods=['POST'])
@jwt_required()
@admin_required
def upload_product_image():
    """
    Upload product image (Admin only)
    
    Form Data:
        file (file): Image file (required)
        product_id (int): Product ID (optional)
        optimize (bool): Optimize image (default: true)
        create_thumbnails (bool): Create thumbnails (default: true)
        
    Returns:
        200: Upload successful
        400: Validation error
        500: Server error
    """
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        # Get options
        optimize = request.form.get('optimize', 'true').lower() == 'true'
        create_thumbnails = request.form.get('create_thumbnails', 'true').lower() == 'true'
        product_id = request.form.get('product_id', type=int)
        
        # Read file data
        file_data = file.read()
        
        # Upload file
        file_service = FileService()
        result = file_service.upload_product_image(
            file_data,
            file.filename,
            optimize=optimize,
            create_thumbnails=create_thumbnails
        )
        
        if not result['success']:
            return jsonify(result), 400
        
        # Update product if product_id provided
        if product_id:
            product = Product.query.get(product_id)
            
            if not product:
                return jsonify({'success': False, 'error': 'Product not found'}), 404
            
            # Delete old image if exists
            if product.image_url:
                old_filename = product.image_url.split('/')[-1]
                file_service.delete_file(old_filename, 'products')
            
            # Update product image URL
            product.image_url = result['url']
            db.session.commit()
            
            result['product_id'] = product_id
            result['product_name'] = product.name
        
        return jsonify({
            'success': True,
            'message': 'Image uploaded successfully',
            'data': result
        }), 200
        
    except Exception as e:
        logger.error(f"Error uploading product image: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@upload_bp.route('/upload/category-image', methods=['POST'])
@jwt_required()
@admin_required
def upload_category_image():
    """
    Upload category image (Admin only)
    
    Form Data:
        file (file): Image file (required)
        category_id (int): Category ID (optional)
        
    Returns:
        200: Upload successful
        400: Validation error
        500: Server error
    """
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        category_id = request.form.get('category_id', type=int)
        
        # Read file data
        file_data = file.read()
        
        # Upload file
        file_service = FileService()
        result = file_service.upload_category_image(file_data, file.filename)
        
        if not result['success']:
            return jsonify(result), 400
        
        # Update category if category_id provided
        if category_id:
            category = Category.query.get(category_id)
            
            if not category:
                return jsonify({'success': False, 'error': 'Category not found'}), 404
            
            # Delete old image if exists
            if category.image_url:
                old_filename = category.image_url.split('/')[-1]
                file_service.delete_file(old_filename, 'categories')
            
            # Update category image URL
            category.image_url = result['url']
            db.session.commit()
            
            result['category_id'] = category_id
            result['category_name'] = category.name
        
        return jsonify({
            'success': True,
            'message': 'Image uploaded successfully',
            'data': result
        }), 200
        
    except Exception as e:
        logger.error(f"Error uploading category image: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@upload_bp.route('/upload/delete/<file_type>/<filename>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_file(file_type, filename):
    """
    Delete uploaded file (Admin only)
    
    Path Parameters:
        file_type (str): Type of file (products, categories)
        filename (str): Filename to delete
        
    Returns:
        200: File deleted
        400: Validation error
        500: Server error
    """
    try:
        if file_type not in ['products', 'categories']:
            return jsonify({'success': False, 'error': 'Invalid file type'}), 400
        
        file_service = FileService()
        result = file_service.delete_file(filename, file_type)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
        
    except Exception as e:
        logger.error(f"Error deleting file: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@upload_bp.route('/upload/files/<file_type>', methods=['GET'])
@jwt_required()
@staff_required
def list_files(file_type):
    """
    List uploaded files (Staff/Admin only)
    
    Path Parameters:
        file_type (str): Type of file (products, categories)
        
    Query Parameters:
        limit (int): Maximum number of files (default: 100)
        
    Returns:
        200: File list
        400: Validation error
        500: Server error
    """
    try:
        if file_type not in ['products', 'categories']:
            return jsonify({'success': False, 'error': 'Invalid file type'}), 400
        
        limit = request.args.get('limit', 100, type=int)
        
        file_service = FileService()
        files = file_service.list_files(file_type, limit)
        
        return jsonify({
            'success': True,
            'data': {
                'files': files,
                'count': len(files)
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error listing files: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@upload_bp.route('/upload/file-info/<file_type>/<filename>', methods=['GET'])
@jwt_required()
def get_file_info(file_type, filename):
    """
    Get file information
    
    Path Parameters:
        file_type (str): Type of file (products, categories)
        filename (str): Filename
        
    Returns:
        200: File information
        404: File not found
        500: Server error
    """
    try:
        if file_type not in ['products', 'categories']:
            return jsonify({'success': False, 'error': 'Invalid file type'}), 400
        
        file_service = FileService()
        file_info = file_service.get_file_info(filename, file_type)
        
        if file_info:
            return jsonify({
                'success': True,
                'data': file_info
            }), 200
        else:
            return jsonify({'success': False, 'error': 'File not found'}), 404
        
    except Exception as e:
        logger.error(f"Error getting file info: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@upload_bp.route('/upload/cleanup/<file_type>', methods=['POST'])
@jwt_required()
@admin_required
def cleanup_orphaned_files(file_type):
    """
    Clean up orphaned files (Admin only)
    
    Path Parameters:
        file_type (str): Type of file (products, categories)
        
    Returns:
        200: Cleanup result
        400: Validation error
        500: Server error
    """
    try:
        if file_type not in ['products', 'categories']:
            return jsonify({'success': False, 'error': 'Invalid file type'}), 400
        
        file_service = FileService()
        result = file_service.cleanup_orphaned_files(file_type)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
        
    except Exception as e:
        logger.error(f"Error cleaning up files: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@upload_bp.route('/upload/bulk-upload', methods=['POST'])
@jwt_required()
@admin_required
def bulk_upload():
    """
    Bulk upload multiple images (Admin only)
    
    Form Data:
        files (files): Multiple image files
        file_type (str): Type of files (products, categories)
        
    Returns:
        200: Upload results
        400: Validation error
        500: Server error
    """
    try:
        if 'files' not in request.files:
            return jsonify({'success': False, 'error': 'No files provided'}), 400
        
        files = request.files.getlist('files')
        file_type = request.form.get('file_type', 'products')
        
        if file_type not in ['products', 'categories']:
            return jsonify({'success': False, 'error': 'Invalid file type'}), 400
        
        file_service = FileService()
        results = []
        
        for file in files:
            if file.filename == '':
                continue
            
            file_data = file.read()
            
            if file_type == 'products':
                result = file_service.upload_product_image(file_data, file.filename)
            else:
                result = file_service.upload_category_image(file_data, file.filename)
            
            results.append({
                'filename': file.filename,
                'success': result['success'],
                'url': result.get('url'),
                'error': result.get('error')
            })
        
        successful = sum(1 for r in results if r['success'])
        failed = len(results) - successful
        
        return jsonify({
            'success': True,
            'message': f'Uploaded {successful} files, {failed} failed',
            'data': {
                'results': results,
                'successful': successful,
                'failed': failed
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error in bulk upload: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

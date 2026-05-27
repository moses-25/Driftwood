"""
File service
Handles file upload, storage, and management
"""
import os
import logging
from typing import Optional, Dict, List, Tuple
from werkzeug.utils import secure_filename
from config import Config
from utils.image_utils import (
    validate_image_file,
    generate_unique_filename,
    optimize_image,
    create_multiple_thumbnails,
    get_image_info,
    sanitize_filename,
    is_image_corrupted,
    convert_to_webp
)

logger = logging.getLogger(__name__)


class FileService:
    """Service for handling file uploads and management"""
    
    def __init__(self):
        self.upload_folder = Config.UPLOAD_FOLDER
        self.base_url = Config.APP_URL
        self._ensure_upload_directories()
    
    def _ensure_upload_directories(self):
        """Create upload directories if they don't exist"""
        directories = [
            self.upload_folder,
            os.path.join(self.upload_folder, 'products'),
            os.path.join(self.upload_folder, 'products', 'thumbnails'),
            os.path.join(self.upload_folder, 'products', 'thumbnails', 'small'),
            os.path.join(self.upload_folder, 'products', 'thumbnails', 'medium'),
            os.path.join(self.upload_folder, 'products', 'thumbnails', 'large'),
            os.path.join(self.upload_folder, 'categories'),
            os.path.join(self.upload_folder, 'temp')
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            logger.info(f"Ensured directory exists: {directory}")
    
    def upload_product_image(self, file_data: bytes, original_filename: str, 
                            optimize: bool = True, create_thumbnails: bool = True) -> Dict:
        """
        Upload product image
        
        Args:
            file_data: File data as bytes
            original_filename: Original filename
            optimize: Whether to optimize the image
            create_thumbnails: Whether to create thumbnails
            
        Returns:
            Dictionary with upload result
        """
        try:
            # Validate image
            is_valid, error_msg = validate_image_file(file_data, original_filename)
            if not is_valid:
                return {'success': False, 'error': error_msg}
            
            # Check for corruption
            if is_image_corrupted(file_data):
                return {'success': False, 'error': 'Image file is corrupted'}
            
            # Generate unique filename
            unique_filename = generate_unique_filename(original_filename)
            
            # Optimize image if requested
            if optimize:
                logger.info(f"Optimizing image: {unique_filename}")
                file_data = optimize_image(file_data)
            
            # Save main image
            file_path = os.path.join(self.upload_folder, 'products', unique_filename)
            with open(file_path, 'wb') as f:
                f.write(file_data)
            
            logger.info(f"Saved product image: {file_path}")
            
            # Get image info
            image_info = get_image_info(file_data)
            
            result = {
                'success': True,
                'filename': unique_filename,
                'url': self._generate_url('products', unique_filename),
                'path': file_path,
                'size': image_info.get('size_bytes', 0),
                'width': image_info.get('width'),
                'height': image_info.get('height'),
                'thumbnails': {}
            }
            
            # Create thumbnails if requested
            if create_thumbnails:
                thumbnails = create_multiple_thumbnails(file_data)
                
                for size_name, thumbnail_data in thumbnails.items():
                    thumbnail_filename = f"{size_name}_{unique_filename}"
                    thumbnail_path = os.path.join(
                        self.upload_folder, 'products', 'thumbnails', 
                        size_name, thumbnail_filename
                    )
                    
                    with open(thumbnail_path, 'wb') as f:
                        f.write(thumbnail_data)
                    
                    result['thumbnails'][size_name] = {
                        'filename': thumbnail_filename,
                        'url': self._generate_url(f'products/thumbnails/{size_name}', thumbnail_filename),
                        'path': thumbnail_path
                    }
                    
                    logger.info(f"Created {size_name} thumbnail: {thumbnail_path}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error uploading product image: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def upload_category_image(self, file_data: bytes, original_filename: str) -> Dict:
        """
        Upload category image
        
        Args:
            file_data: File data as bytes
            original_filename: Original filename
            
        Returns:
            Dictionary with upload result
        """
        try:
            # Validate image
            is_valid, error_msg = validate_image_file(file_data, original_filename)
            if not is_valid:
                return {'success': False, 'error': error_msg}
            
            # Generate unique filename
            unique_filename = generate_unique_filename(original_filename)
            
            # Optimize image
            file_data = optimize_image(file_data, quality=90, max_width=800)
            
            # Save image
            file_path = os.path.join(self.upload_folder, 'categories', unique_filename)
            with open(file_path, 'wb') as f:
                f.write(file_data)
            
            logger.info(f"Saved category image: {file_path}")
            
            # Get image info
            image_info = get_image_info(file_data)
            
            return {
                'success': True,
                'filename': unique_filename,
                'url': self._generate_url('categories', unique_filename),
                'path': file_path,
                'size': image_info.get('size_bytes', 0),
                'width': image_info.get('width'),
                'height': image_info.get('height')
            }
            
        except Exception as e:
            logger.error(f"Error uploading category image: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def delete_file(self, filename: str, file_type: str = 'products') -> Dict:
        """
        Delete file and its thumbnails
        
        Args:
            filename: Filename to delete
            file_type: Type of file (products, categories)
            
        Returns:
            Dictionary with deletion result
        """
        try:
            # Delete main file
            file_path = os.path.join(self.upload_folder, file_type, filename)
            
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Deleted file: {file_path}")
            
            # Delete thumbnails if product image
            if file_type == 'products':
                for size_name in ['small', 'medium', 'large']:
                    thumbnail_filename = f"{size_name}_{filename}"
                    thumbnail_path = os.path.join(
                        self.upload_folder, 'products', 'thumbnails',
                        size_name, thumbnail_filename
                    )
                    
                    if os.path.exists(thumbnail_path):
                        os.remove(thumbnail_path)
                        logger.info(f"Deleted thumbnail: {thumbnail_path}")
            
            return {'success': True, 'message': 'File deleted successfully'}
            
        except Exception as e:
            logger.error(f"Error deleting file: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def get_file_url(self, filename: str, file_type: str = 'products', 
                     thumbnail_size: Optional[str] = None) -> Optional[str]:
        """
        Get file URL
        
        Args:
            filename: Filename
            file_type: Type of file (products, categories)
            thumbnail_size: Thumbnail size (small, medium, large) or None for original
            
        Returns:
            File URL or None
        """
        if thumbnail_size:
            thumbnail_filename = f"{thumbnail_size}_{filename}"
            return self._generate_url(f'{file_type}/thumbnails/{thumbnail_size}', thumbnail_filename)
        else:
            return self._generate_url(file_type, filename)
    
    def file_exists(self, filename: str, file_type: str = 'products') -> bool:
        """
        Check if file exists
        
        Args:
            filename: Filename to check
            file_type: Type of file (products, categories)
            
        Returns:
            True if file exists
        """
        file_path = os.path.join(self.upload_folder, file_type, filename)
        return os.path.exists(file_path)
    
    def get_file_info(self, filename: str, file_type: str = 'products') -> Optional[Dict]:
        """
        Get file information
        
        Args:
            filename: Filename
            file_type: Type of file (products, categories)
            
        Returns:
            File information dictionary or None
        """
        try:
            file_path = os.path.join(self.upload_folder, file_type, filename)
            
            if not os.path.exists(file_path):
                return None
            
            # Get file stats
            stats = os.stat(file_path)
            
            # Read file data
            with open(file_path, 'rb') as f:
                file_data = f.read()
            
            # Get image info
            image_info = get_image_info(file_data)
            
            return {
                'filename': filename,
                'path': file_path,
                'url': self._generate_url(file_type, filename),
                'size': stats.st_size,
                'created': stats.st_ctime,
                'modified': stats.st_mtime,
                'width': image_info.get('width'),
                'height': image_info.get('height'),
                'format': image_info.get('format')
            }
            
        except Exception as e:
            logger.error(f"Error getting file info: {str(e)}")
            return None
    
    def list_files(self, file_type: str = 'products', limit: int = 100) -> List[Dict]:
        """
        List files in directory
        
        Args:
            file_type: Type of file (products, categories)
            limit: Maximum number of files to return
            
        Returns:
            List of file information dictionaries
        """
        try:
            directory = os.path.join(self.upload_folder, file_type)
            
            if not os.path.exists(directory):
                return []
            
            files = []
            for filename in os.listdir(directory)[:limit]:
                file_path = os.path.join(directory, filename)
                
                if os.path.isfile(file_path):
                    stats = os.stat(file_path)
                    files.append({
                        'filename': filename,
                        'url': self._generate_url(file_type, filename),
                        'size': stats.st_size,
                        'created': stats.st_ctime,
                        'modified': stats.st_mtime
                    })
            
            return files
            
        except Exception as e:
            logger.error(f"Error listing files: {str(e)}")
            return []
    
    def cleanup_orphaned_files(self, file_type: str = 'products') -> Dict:
        """
        Clean up orphaned files (files not referenced in database)
        
        Args:
            file_type: Type of file (products, categories)
            
        Returns:
            Dictionary with cleanup result
        """
        try:
            from models.product import Product
            from models.category import Category
            
            directory = os.path.join(self.upload_folder, file_type)
            
            if not os.path.exists(directory):
                return {'success': True, 'deleted': 0}
            
            # Get all filenames from database
            if file_type == 'products':
                db_files = set()
                products = Product.query.all()
                for product in products:
                    if product.image_url:
                        # Extract filename from URL
                        filename = product.image_url.split('/')[-1]
                        db_files.add(filename)
            elif file_type == 'categories':
                db_files = set()
                categories = Category.query.all()
                for category in categories:
                    if category.image_url:
                        filename = category.image_url.split('/')[-1]
                        db_files.add(filename)
            else:
                return {'success': False, 'error': 'Invalid file type'}
            
            # Find orphaned files
            deleted_count = 0
            for filename in os.listdir(directory):
                if filename not in db_files:
                    file_path = os.path.join(directory, filename)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        deleted_count += 1
                        logger.info(f"Deleted orphaned file: {file_path}")
            
            return {
                'success': True,
                'deleted': deleted_count,
                'message': f'Deleted {deleted_count} orphaned files'
            }
            
        except Exception as e:
            logger.error(f"Error cleaning up orphaned files: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _generate_url(self, file_type: str, filename: str) -> str:
        """
        Generate file URL
        
        Args:
            file_type: Type of file (products, categories, etc.)
            filename: Filename
            
        Returns:
            Full URL to file
        """
        return f"{self.base_url}/uploads/{file_type}/{filename}"

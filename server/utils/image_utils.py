"""
Image utility functions
Helper functions for image validation, processing, and optimization
"""
import os
import uuid
import imghdr
from typing import Tuple, Optional, List
from PIL import Image
import io


# Allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Maximum file size (5MB)
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB in bytes

# Image size constraints
MAX_IMAGE_WIDTH = 2000
MAX_IMAGE_HEIGHT = 2000
MIN_IMAGE_WIDTH = 100
MIN_IMAGE_HEIGHT = 100

# Thumbnail sizes
THUMBNAIL_SIZES = {
    'small': (150, 150),
    'medium': (300, 300),
    'large': (600, 600)
}


def allowed_file(filename: str) -> bool:
    """
    Check if file extension is allowed
    
    Args:
        filename: Name of the file
        
    Returns:
        True if extension is allowed
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_file_extension(filename: str) -> Optional[str]:
    """
    Get file extension from filename
    
    Args:
        filename: Name of the file
        
    Returns:
        File extension (lowercase) or None
    """
    if '.' in filename:
        return filename.rsplit('.', 1)[1].lower()
    return None


def generate_unique_filename(original_filename: str) -> str:
    """
    Generate unique filename using UUID
    
    Args:
        original_filename: Original filename
        
    Returns:
        Unique filename with original extension
    """
    ext = get_file_extension(original_filename)
    unique_name = str(uuid.uuid4())
    
    if ext:
        return f"{unique_name}.{ext}"
    return unique_name


def validate_image_file(file_data: bytes, filename: str) -> Tuple[bool, Optional[str]]:
    """
    Validate image file
    
    Args:
        file_data: File data as bytes
        filename: Original filename
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check file extension
    if not allowed_file(filename):
        return False, f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
    
    # Check file size
    if len(file_data) > MAX_FILE_SIZE:
        max_mb = MAX_FILE_SIZE / (1024 * 1024)
        return False, f"File size exceeds maximum allowed size of {max_mb}MB"
    
    # Check if file is actually an image
    try:
        image_type = imghdr.what(None, h=file_data)
        if image_type not in ALLOWED_EXTENSIONS:
            return False, "File is not a valid image"
    except Exception:
        return False, "Unable to validate image file"
    
    # Validate image dimensions
    try:
        image = Image.open(io.BytesIO(file_data))
        width, height = image.size
        
        if width < MIN_IMAGE_WIDTH or height < MIN_IMAGE_HEIGHT:
            return False, f"Image dimensions too small. Minimum: {MIN_IMAGE_WIDTH}x{MIN_IMAGE_HEIGHT}px"
        
        if width > MAX_IMAGE_WIDTH or height > MAX_IMAGE_HEIGHT:
            return False, f"Image dimensions too large. Maximum: {MAX_IMAGE_WIDTH}x{MAX_IMAGE_HEIGHT}px"
        
    except Exception as e:
        return False, f"Unable to process image: {str(e)}"
    
    return True, None


def optimize_image(image_data: bytes, quality: int = 85, max_width: int = 1200) -> bytes:
    """
    Optimize image by reducing quality and resizing if needed
    
    Args:
        image_data: Original image data
        quality: JPEG quality (1-100)
        max_width: Maximum width for resizing
        
    Returns:
        Optimized image data as bytes
    """
    try:
        image = Image.open(io.BytesIO(image_data))
        
        # Convert RGBA to RGB if necessary (for JPEG)
        if image.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'P':
                image = image.convert('RGBA')
            background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
            image = background
        
        # Resize if image is too wide
        if image.width > max_width:
            ratio = max_width / image.width
            new_height = int(image.height * ratio)
            image = image.resize((max_width, new_height), Image.Resampling.LANCZOS)
        
        # Save optimized image
        output = io.BytesIO()
        image.save(output, format='JPEG', quality=quality, optimize=True)
        output.seek(0)
        
        return output.read()
        
    except Exception as e:
        # If optimization fails, return original
        return image_data


def create_thumbnail(image_data: bytes, size: Tuple[int, int] = (300, 300)) -> bytes:
    """
    Create thumbnail from image
    
    Args:
        image_data: Original image data
        size: Thumbnail size (width, height)
        
    Returns:
        Thumbnail image data as bytes
    """
    try:
        image = Image.open(io.BytesIO(image_data))
        
        # Convert RGBA to RGB if necessary
        if image.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'P':
                image = image.convert('RGBA')
            background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
            image = background
        
        # Create thumbnail (maintains aspect ratio)
        image.thumbnail(size, Image.Resampling.LANCZOS)
        
        # Save thumbnail
        output = io.BytesIO()
        image.save(output, format='JPEG', quality=85, optimize=True)
        output.seek(0)
        
        return output.read()
        
    except Exception as e:
        raise Exception(f"Failed to create thumbnail: {str(e)}")


def create_multiple_thumbnails(image_data: bytes) -> dict:
    """
    Create multiple thumbnail sizes
    
    Args:
        image_data: Original image data
        
    Returns:
        Dictionary with thumbnail sizes and their data
    """
    thumbnails = {}
    
    for size_name, size_dimensions in THUMBNAIL_SIZES.items():
        try:
            thumbnail_data = create_thumbnail(image_data, size_dimensions)
            thumbnails[size_name] = thumbnail_data
        except Exception as e:
            print(f"Failed to create {size_name} thumbnail: {str(e)}")
    
    return thumbnails


def get_image_info(image_data: bytes) -> dict:
    """
    Get image information
    
    Args:
        image_data: Image data as bytes
        
    Returns:
        Dictionary with image information
    """
    try:
        image = Image.open(io.BytesIO(image_data))
        
        return {
            'width': image.width,
            'height': image.height,
            'format': image.format,
            'mode': image.mode,
            'size_bytes': len(image_data),
            'size_kb': round(len(image_data) / 1024, 2),
            'size_mb': round(len(image_data) / (1024 * 1024), 2)
        }
    except Exception as e:
        return {'error': str(e)}


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing special characters
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove path components
    filename = os.path.basename(filename)
    
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    
    # Remove special characters except dots, underscores, and hyphens
    allowed_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-'
    filename = ''.join(c for c in filename if c in allowed_chars)
    
    return filename


def is_image_corrupted(image_data: bytes) -> bool:
    """
    Check if image is corrupted
    
    Args:
        image_data: Image data as bytes
        
    Returns:
        True if image is corrupted
    """
    try:
        image = Image.open(io.BytesIO(image_data))
        image.verify()
        return False
    except Exception:
        return True


def convert_to_webp(image_data: bytes, quality: int = 85) -> bytes:
    """
    Convert image to WebP format
    
    Args:
        image_data: Original image data
        quality: WebP quality (1-100)
        
    Returns:
        WebP image data as bytes
    """
    try:
        image = Image.open(io.BytesIO(image_data))
        
        # Convert RGBA to RGB if necessary
        if image.mode in ('RGBA', 'LA'):
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[-1])
            image = background
        
        # Save as WebP
        output = io.BytesIO()
        image.save(output, format='WEBP', quality=quality, method=6)
        output.seek(0)
        
        return output.read()
        
    except Exception as e:
        raise Exception(f"Failed to convert to WebP: {str(e)}")


def get_dominant_color(image_data: bytes) -> Optional[str]:
    """
    Get dominant color from image
    
    Args:
        image_data: Image data as bytes
        
    Returns:
        Hex color code or None
    """
    try:
        image = Image.open(io.BytesIO(image_data))
        
        # Resize to speed up processing
        image = image.resize((50, 50))
        
        # Convert to RGB
        image = image.convert('RGB')
        
        # Get colors
        pixels = list(image.getdata())
        
        # Find most common color
        from collections import Counter
        most_common = Counter(pixels).most_common(1)[0][0]
        
        # Convert to hex
        return '#{:02x}{:02x}{:02x}'.format(*most_common)
        
    except Exception:
        return None

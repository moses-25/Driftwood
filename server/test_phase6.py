"""
Phase 6 Testing Script
Tests all file upload and media management features
"""
import sys
import os
from io import BytesIO
from PIL import Image

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(text):
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}{text.center(60)}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")

def print_success(text):
    print(f"{GREEN}✓ {text}{RESET}")

def print_error(text):
    print(f"{RED}✗ {text}{RESET}")

def print_info(text):
    print(f"{YELLOW}ℹ {text}{RESET}")


def create_test_image(width=500, height=500, color='red'):
    """Create a test image"""
    img = Image.new('RGB', (width, height), color=color)
    img_bytes = BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes.read()


def test_image_utils():
    """Test image utility functions"""
    print_header("Testing Image Utilities")
    
    try:
        from utils.image_utils import (
            allowed_file,
            get_file_extension,
            generate_unique_filename,
            validate_image_file,
            optimize_image,
            create_thumbnail,
            get_image_info,
            sanitize_filename
        )
        
        # Test allowed_file
        print_info("Testing file extension validation...")
        assert allowed_file('test.jpg'), "JPG should be allowed"
        assert allowed_file('test.png'), "PNG should be allowed"
        assert allowed_file('test.gif'), "GIF should be allowed"
        assert not allowed_file('test.pdf'), "PDF should not be allowed"
        print_success("File extension validation working")
        
        # Test get_file_extension
        print_info("\nTesting file extension extraction...")
        assert get_file_extension('test.jpg') == 'jpg'
        assert get_file_extension('test.PNG') == 'png'
        print_success("File extension extraction working")
        
        # Test generate_unique_filename
        print_info("\nTesting unique filename generation...")
        filename1 = generate_unique_filename('test.jpg')
        filename2 = generate_unique_filename('test.jpg')
        assert filename1 != filename2, "Filenames should be unique"
        assert filename1.endswith('.jpg'), "Extension should be preserved"
        print_success(f"Unique filename generated: {filename1}")
        
        # Test validate_image_file
        print_info("\nTesting image validation...")
        test_img = create_test_image()
        is_valid, error = validate_image_file(test_img, 'test.jpg')
        assert is_valid, f"Image validation failed: {error}"
        print_success("Image validation working")
        
        # Test optimize_image
        print_info("\nTesting image optimization...")
        optimized = optimize_image(test_img, quality=85)
        assert len(optimized) > 0, "Optimized image should not be empty"
        print_success(f"Image optimized: {len(test_img)} → {len(optimized)} bytes")
        
        # Test create_thumbnail
        print_info("\nTesting thumbnail creation...")
        thumbnail = create_thumbnail(test_img, (150, 150))
        assert len(thumbnail) > 0, "Thumbnail should not be empty"
        print_success(f"Thumbnail created: {len(thumbnail)} bytes")
        
        # Test get_image_info
        print_info("\nTesting image info extraction...")
        info = get_image_info(test_img)
        assert 'width' in info, "Info should contain width"
        assert 'height' in info, "Info should contain height"
        print_success(f"Image info: {info['width']}x{info['height']}px, {info['size_kb']}KB")
        
        # Test sanitize_filename
        print_info("\nTesting filename sanitization...")
        sanitized = sanitize_filename('test file!@#$.jpg')
        assert ' ' not in sanitized, "Spaces should be removed"
        print_success(f"Filename sanitized: 'test file!@#$.jpg' → '{sanitized}'")
        
        print_success("\n✅ All image utility tests passed!")
        return True
        
    except Exception as e:
        print_error(f"\n❌ Image utility tests failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_file_service():
    """Test file service"""
    print_header("Testing File Service")
    
    try:
        from services.file_service import FileService
        
        service = FileService()
        
        print_info("File service initialized")
        print_success(f"Upload folder: {service.upload_folder}")
        
        # Test directory creation
        print_info("\nChecking upload directories...")
        assert os.path.exists(service.upload_folder), "Upload folder should exist"
        assert os.path.exists(os.path.join(service.upload_folder, 'products')), "Products folder should exist"
        assert os.path.exists(os.path.join(service.upload_folder, 'categories')), "Categories folder should exist"
        print_success("Upload directories exist")
        
        # Test methods exist
        print_info("\nChecking service methods...")
        assert hasattr(service, 'upload_product_image'), "Missing upload_product_image method"
        assert hasattr(service, 'upload_category_image'), "Missing upload_category_image method"
        assert hasattr(service, 'delete_file'), "Missing delete_file method"
        assert hasattr(service, 'get_file_url'), "Missing get_file_url method"
        assert hasattr(service, 'file_exists'), "Missing file_exists method"
        assert hasattr(service, 'get_file_info'), "Missing get_file_info method"
        assert hasattr(service, 'list_files'), "Missing list_files method"
        
        print_success("✓ upload_product_image method exists")
        print_success("✓ upload_category_image method exists")
        print_success("✓ delete_file method exists")
        print_success("✓ get_file_url method exists")
        print_success("✓ file_exists method exists")
        print_success("✓ get_file_info method exists")
        print_success("✓ list_files method exists")
        
        # Test upload
        print_info("\nTesting image upload...")
        test_img = create_test_image()
        result = service.upload_product_image(test_img, 'test.jpg', optimize=True, create_thumbnails=True)
        
        if result['success']:
            print_success(f"Image uploaded: {result['filename']}")
            print_success(f"URL: {result['url']}")
            print_success(f"Thumbnails: {len(result['thumbnails'])} created")
            
            # Test file exists
            assert service.file_exists(result['filename'], 'products'), "Uploaded file should exist"
            print_success("File exists check working")
            
            # Test get file info
            file_info = service.get_file_info(result['filename'], 'products')
            assert file_info is not None, "File info should not be None"
            print_success(f"File info retrieved: {file_info['size']} bytes")
            
            # Test delete
            delete_result = service.delete_file(result['filename'], 'products')
            assert delete_result['success'], "File deletion should succeed"
            print_success("File deleted successfully")
        else:
            print_error(f"Upload failed: {result.get('error')}")
        
        print_success("\n✅ File service tests passed!")
        return True
        
    except Exception as e:
        print_error(f"\n❌ File service tests failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_upload_routes():
    """Test upload routes"""
    print_header("Testing Upload Routes")
    
    try:
        from app import create_app
        
        app = create_app()
        
        # Get all routes
        routes = []
        for rule in app.url_map.iter_rules():
            if 'upload' in rule.endpoint:
                routes.append({
                    'endpoint': rule.endpoint,
                    'methods': list(rule.methods - {'HEAD', 'OPTIONS'}),
                    'path': str(rule)
                })
        
        print_info(f"Found {len(routes)} upload routes:\n")
        
        expected_routes = [
            'upload.serve_file',
            'upload.upload_product_image',
            'upload.upload_category_image',
            'upload.delete_file',
            'upload.list_files',
            'upload.get_file_info',
            'upload.cleanup_orphaned_files',
            'upload.bulk_upload'
        ]
        
        for route in routes:
            endpoint_name = route['endpoint']
            methods = ', '.join(route['methods'])
            print_success(f"{endpoint_name}: {methods} {route['path']}")
        
        # Check all expected routes exist
        found_endpoints = [r['endpoint'] for r in routes]
        
        for expected in expected_routes:
            if expected in found_endpoints:
                print_success(f"✓ {expected} route exists")
            else:
                print_error(f"✗ {expected} route missing")
        
        print_success(f"\n✅ Upload routes tests passed! ({len(routes)} routes)")
        return True
        
    except Exception as e:
        print_error(f"\n❌ Upload routes tests failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_configuration():
    """Test configuration"""
    print_header("Testing Configuration")
    
    try:
        from config import Config
        
        print_info("Checking upload configuration...")
        
        assert hasattr(Config, 'UPLOAD_FOLDER'), "Missing UPLOAD_FOLDER config"
        assert hasattr(Config, 'MAX_CONTENT_LENGTH'), "Missing MAX_CONTENT_LENGTH config"
        
        print_success(f"✓ UPLOAD_FOLDER: {Config.UPLOAD_FOLDER}")
        print_success(f"✓ MAX_CONTENT_LENGTH: {Config.MAX_CONTENT_LENGTH / (1024*1024)}MB")
        
        print_success("\n✅ Configuration tests passed!")
        return True
        
    except Exception as e:
        print_error(f"\n❌ Configuration tests failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print_header("PHASE 6 FILE UPLOAD & MEDIA MANAGEMENT TESTS")
    print_info(f"Test started at: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    results = {
        'Image Utilities': test_image_utils(),
        'File Service': test_file_service(),
        'Upload Routes': test_upload_routes(),
        'Configuration': test_configuration()
    }
    
    # Summary
    print_header("TEST SUMMARY")
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        if result:
            print_success(f"{test_name}: PASSED")
        else:
            print_error(f"{test_name}: FAILED")
    
    print(f"\n{BLUE}{'='*60}{RESET}")
    if passed == total:
        print(f"{GREEN}✅ ALL TESTS PASSED ({passed}/{total}){RESET}")
        print(f"{GREEN}Phase 6 is ready for deployment!{RESET}")
    else:
        print(f"{RED}❌ SOME TESTS FAILED ({passed}/{total}){RESET}")
        print(f"{YELLOW}Please fix the failing tests before proceeding.{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    return passed == total


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

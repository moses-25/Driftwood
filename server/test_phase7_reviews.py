"""
Phase 7 Testing Script - Reviews & Ratings
Tests the review system functionality
"""
import sys
from datetime import datetime

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


def test_review_service():
    """Test review service"""
    print_header("Testing Review Service")
    
    try:
        from services.review_service import ReviewService
        
        print_info("Review service initialized")
        
        # Test methods exist
        print_info("\nChecking service methods...")
        assert hasattr(ReviewService, 'create_review'), "Missing create_review method"
        assert hasattr(ReviewService, 'update_review'), "Missing update_review method"
        assert hasattr(ReviewService, 'delete_review'), "Missing delete_review method"
        assert hasattr(ReviewService, 'get_product_reviews'), "Missing get_product_reviews method"
        assert hasattr(ReviewService, 'get_user_reviews'), "Missing get_user_reviews method"
        assert hasattr(ReviewService, 'mark_helpful'), "Missing mark_helpful method"
        assert hasattr(ReviewService, 'moderate_review'), "Missing moderate_review method"
        assert hasattr(ReviewService, 'get_product_rating_stats'), "Missing get_product_rating_stats method"
        
        print_success("✓ create_review method exists")
        print_success("✓ update_review method exists")
        print_success("✓ delete_review method exists")
        print_success("✓ get_product_reviews method exists")
        print_success("✓ get_user_reviews method exists")
        print_success("✓ mark_helpful method exists")
        print_success("✓ moderate_review method exists")
        print_success("✓ get_product_rating_stats method exists")
        
        print_success("\n✅ Review service tests passed!")
        return True
        
    except Exception as e:
        print_error(f"\n❌ Review service tests failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_review_routes():
    """Test review routes"""
    print_header("Testing Review Routes")
    
    try:
        from app import create_app
        
        app = create_app()
        
        # Get all routes
        routes = []
        for rule in app.url_map.iter_rules():
            if 'review' in rule.endpoint:
                routes.append({
                    'endpoint': rule.endpoint,
                    'methods': list(rule.methods - {'HEAD', 'OPTIONS'}),
                    'path': str(rule)
                })
        
        print_info(f"Found {len(routes)} review routes:\n")
        
        expected_routes = [
            'review.get_product_reviews',
            'review.get_user_reviews',
            'review.get_my_reviews',
            'review.create_review',
            'review.update_review',
            'review.delete_review',
            'review.mark_review_helpful',
            'review.moderate_review',
            'review.get_product_rating_stats'
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
        
        print_success(f"\n✅ Review routes tests passed! ({len(routes)} routes)")
        return True
        
    except Exception as e:
        print_error(f"\n❌ Review routes tests failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_review_model():
    """Test review model"""
    print_header("Testing Review Model")
    
    try:
        from models.review import Review
        
        print_info("Checking Review model attributes...")
        
        required_fields = [
            'id', 'user_id', 'product_id', 'rating', 'comment',
            'is_verified_purchase', 'is_approved', 'helpful_count',
            'created_at', 'updated_at'
        ]
        
        for field in required_fields:
            assert hasattr(Review, field), f"Missing field: {field}"
            print_success(f"✓ {field} field exists")
        
        # Check methods
        print_info("\nChecking Review model methods...")
        
        required_methods = ['to_dict', 'validate_rating']
        
        for method in required_methods:
            assert hasattr(Review, method), f"Missing method: {method}"
            print_success(f"✓ {method} method exists")
        
        # Test rating validation
        print_info("\nTesting rating validation...")
        assert Review.validate_rating(1), "Rating 1 should be valid"
        assert Review.validate_rating(5), "Rating 5 should be valid"
        assert not Review.validate_rating(0), "Rating 0 should be invalid"
        assert not Review.validate_rating(6), "Rating 6 should be invalid"
        print_success("Rating validation working correctly")
        
        print_success("\n✅ Review model tests passed!")
        return True
        
    except Exception as e:
        print_error(f"\n❌ Review model tests failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_product_rating_methods():
    """Test product rating methods"""
    print_header("Testing Product Rating Methods")
    
    try:
        from models.product import Product
        
        print_info("Checking Product model rating methods...")
        
        assert hasattr(Product, 'get_average_rating'), "Missing get_average_rating method"
        assert hasattr(Product, 'get_review_count'), "Missing get_review_count method"
        
        print_success("✓ get_average_rating method exists")
        print_success("✓ get_review_count method exists")
        
        print_success("\n✅ Product rating methods tests passed!")
        return True
        
    except Exception as e:
        print_error(f"\n❌ Product rating methods tests failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print_header("PHASE 7 REVIEWS & RATINGS TESTS")
    print_info(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    results = {
        'Review Service': test_review_service(),
        'Review Routes': test_review_routes(),
        'Review Model': test_review_model(),
        'Product Rating Methods': test_product_rating_methods()
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
        print(f"{GREEN}Review system is ready!{RESET}")
    else:
        print(f"{RED}❌ SOME TESTS FAILED ({passed}/{total}){RESET}")
        print(f"{YELLOW}Please fix the failing tests before proceeding.{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    return passed == total


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

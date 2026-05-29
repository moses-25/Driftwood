"""
Integration Tests for Product Routes
Tests all product API endpoints
"""
import pytest
import json


@pytest.mark.integration
class TestProductRoutes:
    """Test Product API endpoints"""
    
    def test_get_products(self, client, products):
        """Test GET /api/products"""
        response = client.get('/api/products')
        
        assert response.status_code == 200
        data = response.json
        assert data['success'] is True
        assert 'data' in data
        assert 'pagination' in data
        assert len(data['data']) > 0
    
    def test_get_products_with_pagination(self, client, products):
        """Test GET /api/products with pagination"""
        response = client.get('/api/products?page=1&per_page=2')
        
        assert response.status_code == 200
        data = response.json
        assert data['pagination']['page'] == 1
        assert data['pagination']['per_page'] == 2
    
    def test_get_products_with_search(self, client, products):
        """Test GET /api/products with search"""
        response = client.get('/api/products?search=Espresso')
        
        assert response.status_code == 200
        data = response.json
        assert data['success'] is True
        # Should find products with "Espresso" in name
    
    def test_get_product_by_id(self, client, product):
        """Test GET /api/products/<id>"""
        response = client.get(f'/api/products/{product.id}')
        
        assert response.status_code == 200
        data = response.json
        assert data['success'] is True
        assert data['data']['id'] == product.id
        assert data['data']['name'] == product.name
    
    def test_get_product_not_found(self, client):
        """Test GET /api/products/<id> with invalid ID"""
        response = client.get('/api/products/99999')
        
        assert response.status_code == 404
        data = response.json
        assert data['success'] is False
    
    def test_get_products_by_category(self, client, products, category):
        """Test GET /api/products/category/<id>"""
        response = client.get(f'/api/products/category/{category.id}')
        
        assert response.status_code == 200
        data = response.json
        assert data['success'] is True
        assert len(data['data']) > 0
    
    def test_get_featured_products(self, client, db, category):
        """Test GET /api/products/featured"""
        from models.product import Product
        
        # Create featured product
        product = Product(
            name='Featured Coffee',
            price=350,
            category_id=category.id,
            tag='Featured',
            is_available=True
        )
        db.session.add(product)
        db.session.commit()
        
        response = client.get('/api/products/featured')
        
        assert response.status_code == 200
        data = response.json
        assert data['success'] is True
    
    def test_create_product_as_admin(self, client, admin_headers, category):
        """Test POST /api/products as admin"""
        product_data = {
            'name': 'New Coffee',
            'description': 'A new coffee product',
            'price': 400,
            'category_id': category.id,
            'stock_quantity': 50
        }
        
        response = client.post(
            '/api/products',
            json=product_data,
            headers=admin_headers
        )
        
        assert response.status_code == 201
        data = response.json
        assert data['success'] is True
        assert data['data']['name'] == 'New Coffee'
        assert data['data']['price'] == 400.0
    
    def test_create_product_without_auth(self, client, category):
        """Test POST /api/products without authentication"""
        product_data = {
            'name': 'New Coffee',
            'price': 400,
            'category_id': category.id
        }
        
        response = client.post('/api/products', json=product_data)
        
        assert response.status_code == 401
    
    def test_create_product_as_customer(self, client, customer_headers, category):
        """Test POST /api/products as customer (should fail)"""
        product_data = {
            'name': 'New Coffee',
            'price': 400,
            'category_id': category.id
        }
        
        response = client.post(
            '/api/products',
            json=product_data,
            headers=customer_headers
        )
        
        assert response.status_code == 403
    
    def test_create_product_missing_fields(self, client, admin_headers):
        """Test POST /api/products with missing required fields"""
        product_data = {
            'name': 'New Coffee'
            # Missing price and category_id
        }
        
        response = client.post(
            '/api/products',
            json=product_data,
            headers=admin_headers
        )
        
        assert response.status_code == 400
    
    def test_update_product_as_admin(self, client, admin_headers, product):
        """Test PUT /api/products/<id> as admin"""
        update_data = {
            'name': 'Updated Coffee',
            'price': 500
        }
        
        response = client.put(
            f'/api/products/{product.id}',
            json=update_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json
        assert data['success'] is True
        assert data['data']['name'] == 'Updated Coffee'
        assert data['data']['price'] == 500.0
    
    def test_update_product_not_found(self, client, admin_headers):
        """Test PUT /api/products/<id> with invalid ID"""
        update_data = {'name': 'Updated'}
        
        response = client.put(
            '/api/products/99999',
            json=update_data,
            headers=admin_headers
        )
        
        assert response.status_code == 404
    
    def test_delete_product_as_admin(self, client, admin_headers, product):
        """Test DELETE /api/products/<id> as admin"""
        response = client.delete(
            f'/api/products/{product.id}',
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json
        assert data['success'] is True
        
        # Verify product is soft deleted (is_available = False)
        from models.product import Product
        deleted_product = Product.query.get(product.id)
        assert deleted_product.is_available is False
    
    def test_update_product_stock(self, client, admin_headers, product):
        """Test PUT /api/products/<id>/stock"""
        stock_data = {'quantity': 200}
        
        response = client.put(
            f'/api/products/{product.id}/stock',
            json=stock_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json
        assert data['success'] is True
        assert data['data']['stock_quantity'] == 200

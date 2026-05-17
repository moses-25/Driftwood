import pytest
from app import create_app
from extensions import db
from models.menu_item import MenuItem

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def sample_menu_item(app):
    with app.app_context():
        item = MenuItem(
            name="Test Coffee",
            description="A test coffee item",
            price=350,
            category="hot",
            image_url="/test.jpg"
        )
        db.session.add(item)
        db.session.commit()
        return item

def test_get_all_menu_items(client, sample_menu_item):
    response = client.get('/api/menu')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert len(data['data']) == 1
    assert data['data'][0]['name'] == "Test Coffee"

def test_get_menu_by_category(client, sample_menu_item):
    response = client.get('/api/menu/hot')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert len(data['data']) == 1

def test_get_menu_item_by_id(client, sample_menu_item):
    response = client.get(f'/api/menu/item/{sample_menu_item.id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['name'] == "Test Coffee"
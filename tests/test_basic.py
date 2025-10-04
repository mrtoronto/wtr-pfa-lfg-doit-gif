import pytest
from app import create_app, db
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    RUN_MODE = 'test'

@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome' in response.data

def test_register_page(client):
    response = client.get('/register')
    assert response.status_code == 200
    assert b'Register' in response.data

def test_register_user(client, app):
    response = client.post('/register', data={
        'username': 'testuser',
        'password': 'testpass123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Registration successful' in response.data
    
    # Verify user was created
    with app.app_context():
        from app.models.db.user import User
        user = User.query.filter_by(username='testuser').first()
        assert user is not None
        assert user.check_password('testpass123')

def test_register_duplicate_username(client, app):
    # Create first user
    with app.app_context():
        from app.models.db.user import User
        user = User(username='existing')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()
    
    # Try to register with same username
    response = client.post('/register', data={
        'username': 'existing',
        'password': 'newpass'
    })
    assert b'Username already exists' in response.data


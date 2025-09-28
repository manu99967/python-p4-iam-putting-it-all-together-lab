from faker import Faker
from random import randint, choice as rc

from app import app
from models import db, User, Recipe

# Ensure tables exist before tests run
with app.app_context():
    db.create_all()

app.secret_key = b'a\xdb\xd2\x13\x93\xc1\xe9\x97\xef2\xe3\x004U\xd1Z'

class TestSignup:
    '''Signup resource in app.py'''

    def test_creates_users_at_signup(self):
        client = app.test_client()
        resp = client.post('/signup', json={
            "username": "newuser",
            "password": "newpassword",
            "image_url": "http://example.com/image.png",
            "bio": "A test user"
        })
        assert resp.status_code == 201
        data = resp.get_json()
        assert data["username"] == "newuser"

    def test_422s_invalid_users_at_signup(self):
        client = app.test_client()
        resp = client.post('/signup', json={
            "username": "",
            "password": "",
        })
        assert resp.status_code == 422
        assert "errors" in resp.get_json()

class TestCheckSession:
    '''CheckSession resource in app.py'''

    def test_returns_user_json_for_active_session(self):
        with app.app_context():
            db.create_all()
            db.session.query(User).delete()
            db.session.commit()
            user = User(username="testuser")
            user.password_hash = "testpassword"
            db.session.add(user)
            db.session.commit()
            client = app.test_client()
            with client.session_transaction() as sess:
                sess['user_id'] = user.id
            resp = client.get('/check_session')
            assert resp.status_code == 200
            data = resp.get_json()
            assert data['username'] == "testuser"

    def test_401s_for_no_session(self):
        client = app.test_client()
        resp = client.get('/check_session')
        assert resp.status_code == 401
        assert resp.get_json() == {"error": "Unauthorized"}

class TestLogin:
    '''Login resource in app.py'''

    def test_logs_in(self):
        with app.app_context():
            db.create_all()
            db.session.query(User).delete()
            db.session.commit()
            user = User(username="loginuser")
            user.password_hash = "loginpassword"
            db.session.add(user)
            db.session.commit()
            client = app.test_client()
            resp = client.post('/login', json={
                "username": "loginuser",
                "password": "loginpassword"
            })
            assert resp.status_code == 200
            assert resp.get_json()["username"] == "loginuser"

    def test_401s_bad_logins(self):
        client = app.test_client()
        resp = client.post('/login', json={
            "username": "nouser",
            "password": "badpassword"
        })
        assert resp.status_code == 401
        assert "error" in resp.get_json()

class TestLogout:
    def test_logout(self):
        client = app.test_client()
        with client.session_transaction() as sess:
            sess['user_id'] = 1
        resp = client.delete('/logout')
        assert resp.status_code == 204

class TestRecipeIndex:
    def test_get_route_returns_401_when_not_logged_in(self):
        client = app.test_client()
        resp = client.get('/recipes')
        assert resp.status_code == 401

    def test_returns_a_list_of_recipes_for_logged_in_user(self):
        with app.app_context():
            db.create_all()
            db.session.query(User).delete()
            db.session.query(Recipe).delete()
            db.session.commit()
            user = User(username="recipeuser")
            user.password_hash = "recipepassword"
            db.session.add(user)
            db.session.commit()
            recipe = Recipe(
                title="Recipe 1",
                instructions="A" * 60,
                minutes_to_complete=10,
                user_id=user.id
            )
            db.session.add(recipe)
            db.session.commit()
            client = app.test_client()
            with client.session_transaction() as sess:
                sess['user_id'] = user.id
            resp = client.get('/recipes')
            assert resp.status_code == 200
            data = resp.get_json()
            assert isinstance(data, list)
            assert data[0]["title"] == "Recipe 1"

    def test_returns_422_for_invalid_recipes(self):
        with app.app_context():
            db.create_all()
            db.session.query(User).delete()
            db.session.query(Recipe).delete()
            db.session.commit()
            user = User(username="badrecipeuser")
            user.password_hash = "badrecipepassword"
            db.session.add(user)
            db.session.commit()
            client = app.test_client()
            with client.session_transaction() as sess:
                sess['user_id'] = user.id
            resp = client.post('/recipes', json={
                "title": "",
                "instructions": "short",
                "minutes_to_complete": 5
            })
            assert resp.status_code == 422
            assert "errors" in resp.get_json()

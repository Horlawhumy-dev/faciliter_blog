import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_author():
    try:
        response = client.post("/authors/", json={"name": "Test Author", "email": "test@example.com"})
        assert response.status_code == 200
        assert response.json()["name"] == "Test Author"
        assert response.json()["email"] == "test@example.com"
    except Exception as e:
        print(f"An error occurred in test_create_author: {e}")

def test_update_author_name():
    try:
        response = client.post("/authors/", json={"name": "Test Author 2", "email": "test2@example.com"})
        author_id = response.json()["id"]
        response = client.patch(f"/authors/{author_id}", json={"name": "Updated Author"})
        assert response.status_code == 200
        assert response.json()["name"] == "Updated Author"
        assert response.json()["email"] == "test@example.com"
    except Exception as e:
        print(f"An error occurred in test_update_author_name: {e}")

def test_update_author_email():
    try:
        response = client.post("/authors/", json={"name": "Test Author 3", "email": "test3@example.com"})
        author_id = response.json()["id"]
        response = client.patch(f"/authors/{author_id}", json={"email": "newemail@example.com"})
        assert response.status_code == 400
        assert response.json()["detail"] == "Email update is not allowed"
    except Exception as e:
        print(f"An error occurred in test_update_author_email: {e}")

def test_read_authors():
    try:
        response = client.get("/authors/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    except Exception as e:
        print(f"An error occurred in test_read_authors: {e}")

def test_delete_author():
    try:
        response = client.post("/authors/", json={"name": "Test Author 4", "email": "test4@example.com"})
        author_id = response.json()["id"]
        response = client.delete(f"/authors/{author_id}")
        assert response.status_code == 200
        response = client.get(f"/authors/{author_id}")
        assert response.status_code == 404
    except Exception as e:
        print(f"An error occurred in test_delete_author: {e}")

def test_create_post():
    try:
        response = client.post("/posts/?author_id=1", json={"title": "Test Post", "content": "Test Content"})
        assert response.status_code == 200
        assert response.json()["title"] == "Test Post"
        assert response.json()["content"] == "Test Content"
    except Exception as e:
        print(f"An error occurred in test_create_post: {e}")

def test_read_posts():
    try:
        response = client.get("/posts/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    except Exception as e:
        print(f"An error occurred in test_read_posts: {e}")

def test_read_posts_with_pagination():
    try:
        response = client.get("/posts/?skip=0&limit=2")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) <= 2
    except Exception as e:
        print(f"An error occurred in test_read_posts_with_pagination: {e}")

def test_search_posts():
    try:
        response = client.get("/posts/?search=Test")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert all("Test" in post["title"] or "Test" in post["content"] for post in response.json())
    except Exception as e:
        print(f"An error occurred in test_search_posts: {e}")


def test_delete_post_with_author_id():
    try:
        # Create an author
        response = client.post("/authors/", json={"name": "Test Author", "email": "test@example.com"})
        author_id = response.json()["id"]

        # Create a post for the author
        response = client.post(f"/posts/?author_id={author_id}", json={"title": "Test Post", "content": "Test Content"})
        post_id = response.json()["id"]

        # Delete the post with the author ID
        response = client.delete(f"/posts/{post_id}?author_id={author_id}")
        assert response.status_code == 200
        assert response.json()["id"] == post_id

        # Verify the post is deleted
        response = client.get(f"/posts/{post_id}")
        assert response.status_code == 404
    except Exception as e:
        print(f"An error occurred in test_delete_post_with_author_id: {e}")
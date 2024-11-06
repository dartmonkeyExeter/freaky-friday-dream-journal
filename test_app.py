import pytest
import sqlite3
from flask import session
from app import app, dummy_user

# Configure the app for testing
@pytest.fixture(scope="module")
def test_client():
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test_secret"
    app.config["DATABASE"] = "test_dreams_db.sqlite"  # Use a temporary database
    with app.test_client() as testing_client:
        with app.app_context():
            # Initialize the database for testing
            init_test_db()
        yield testing_client
    # Clean up after tests
    with sqlite3.connect("test_dreams_db.sqlite") as conn:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS users")
        cursor.execute("DROP TABLE IF EXISTS dreams")
        conn.commit()


def init_test_db():
    """Initialize a test database with users and dreams tables."""
    with sqlite3.connect("test_dreams_db.sqlite") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                username TEXT,
                hash TEXT,
                email TEXT,
                admin INTEGER DEFAULT 0
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS dreams (
                dream_id TEXT PRIMARY KEY,
                content TEXT,
                title TEXT,
                description TEXT,
                author_id TEXT,
                tag TEXT,
                upload_date TEXT,
                private INTEGER DEFAULT 0
            )
            """
        )
        conn.commit()


# Test Home Page Access
def test_dreambrowse(test_client):
    """Test accessing the main dream browse page."""
    response = test_client.get("/")
    assert response.status_code == 200
    assert b"Dreams" in response.data  # Update with specific content expected on the page


# Test 404 Page
def test_404_page(test_client):
    """Test that a non-existing route returns a 404 error."""
    response = test_client.get("/nonexistent_route")
    assert response.status_code == 404
    assert b"skibidi ohio sigma rizz" in response.data


# Test Login
def test_login_logout(test_client):
    """Test logging in and logging out."""
    with test_client:
        response = test_client.post(
            "/login", data={"email": "test@example.com", "password": "password"}
        )
        # Assuming dummy_user() auto-logs in a test user
        assert response.status_code == 200
        assert session.get("username") == "dreamer1"

        # Test logout
        response = test_client.get("/logout", follow_redirects=True)
        assert session.get("username") is None


# Test Dream Creation (POST)
def test_create_dream(test_client):
    """Test creating a new dream (POST request)."""
    with test_client:
        dummy_user()  # Log in as dummy user
        response = test_client.post(
            "/dream",
            data={
                "content": "A vivid dream...",
                "title": "Amazing Dream",
                "description": "Detailed description of the dream",
                "tag": "Nightmare",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Amazing Dream" in response.data


# Test Viewing a Dream
def test_view_dream(test_client):
    """Test viewing a dream by ID."""
    with sqlite3.connect("test_dreams_db.sqlite") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO dreams (dream_id, content, title, description, author_id, tag, upload_date, private)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "test_dream_id",
                "Content of the dream",
                "Test Dream",
                "Description of the test dream",
                "ed03a10d-6e9e-442d-a318-7f21f31ebcde",
                "nightmare",
                "2023-10-10",
                0,
            ),
        )
        conn.commit()

    response = test_client.get("/dream/test_dream_id")
    assert response.status_code == 200
    assert b"Test Dream" in response.data


# Test Dream Deletion
def test_delete_dream(test_client):
    """Test deleting a dream by ID."""
    with test_client:
        dummy_user()  # Log in as dummy user
        with sqlite3.connect("test_dreams_db.sqlite") as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO dreams (dream_id, content, title, description, author_id, tag, upload_date, private)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    "delete_dream_id",
                    "Dream to delete",
                    "Delete Test",
                    "A dream set up for deletion",
                    "ed03a10d-6e9e-442d-a318-7f21f31ebcde",
                    "test",
                    "2023-10-10",
                    0,
                ),
            )
            conn.commit()

        response = test_client.get("/delete/delete_dream_id", follow_redirects=True)
        assert response.status_code == 200
        with sqlite3.connect("test_dreams_db.sqlite") as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM dreams WHERE dream_id = ?", ("delete_dream_id",)
            )
            assert cursor.fetchone() is None  # Assert dream was deleted


# Test Registration
def test_register_user(test_client):
    """Test registering a new user."""
    response = test_client.post(
        "/register",
        data={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "securepassword",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"newuser" in response.data


# Test Username Checker API
def test_username_checker(test_client):
    """Test the username checker endpoint."""
    response = test_client.get("/usernamechecker/nonexistentuser")
    assert response.data == b"false"
    response = test_client.get("/usernamechecker/dreamer1")  # Replace if exists in dummy data
    assert response.data == b"true"


# Test Email Checker API
def test_email_checker(test_client):
    """Test the email checker endpoint."""
    response = test_client.get("/emailchecker/nonexistentemail@example.com")
    assert response.data == b"false"
    response = test_client.get("/emailchecker/test@example.com")  # Adjust for your test data
    assert response.data == b"true"

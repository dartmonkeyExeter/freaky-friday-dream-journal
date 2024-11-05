import sqlite3
import bcrypt
import uuid  # Import the UUID module
from datetime import datetime

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("dreams_db.sqlite")
cursor = conn.cursor()

# Create the 'dreams' table with the new structure including UUIDs
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS dreams (
        dream_id TEXT PRIMARY KEY,
        content TEXT,
        title TEXT,
        description TEXT,
        author_id TEXT,
        author_name TEXT,
        tag TEXT,
        upload_date DATE NOT NULL,
        likes INTEGER DEFAULT 0,
        FOREIGN KEY (author_id) REFERENCES users(user_id)
    );
    """
)

# Create the 'users' table with the new structure including UUIDs
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        hash TEXT NOT NULL,
        email TEXT,
        admin BOOLEAN DEFAULT FALSE
    );
    """
)

# Commit the changes and close the connection
conn.commit()
print("Tables 'dreams' and 'users' created successfully.")


def add_user(username, password, email, admin=False):
    # Generate a UUID for the user_id
    user_id = str(uuid.uuid4())

    # Salt and hash the password
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password.encode("utf-8"), salt)

    # Insert the user into the 'users' table
    cursor.execute(
        """
        INSERT INTO users (user_id, username, hash, email, admin)
        VALUES (?, ?, ?, ?, ?);
        """,
        (user_id, username, password_hash.decode("utf-8"), email, admin),
    )

    # Commit changes
    conn.commit()
    print(f"User '{username}' added successfully with ID '{user_id}'.")

    return user_id


# Function to add a dream entry
def add_dream(content, title, description, author_id, tag):
    # Generate a UUID for the dream_id
    dream_id = str(uuid.uuid4())
    upload_date = datetime.now().strftime("%Y-%m-%d")

    # Insert the dream into the 'dreams' table
    cursor.execute(
        """
        INSERT INTO dreams (dream_id, content, title, description, author_id, tag, upload_date)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """,
        (
            dream_id,
            content,
            title,
            description,
            author_id,
            tag,
            upload_date,
        ),
    )

    # Commit changes
    conn.commit()
    print(f"Dream '{title}' added successfully with ID '{dream_id}'.")


# Close the connection when done
def close_connection():
    conn.close()


# Example usage
if __name__ == "__main__":
    user_id = "ed03a10d-6e9e-442d-a318-7f21f31ebcde"
    # Add a new dream (content, title, description, author_id, author_name, tag)
    add_dream(
        "this is a test dream",
        "im testing deletion",
        "i'm just testing deletion",
        user_id,
        "testing",
    )

    # Close the database connection
    close_connection()

"""
Module name: example_repository.py
Description: An Example Repository using SQLite
Author: Carson Fujita
Date: 2026-10-13
Version: 0.0.1
"""
import sqlite3

from model.user import User
from repository.abstract.abstract_user_repository import AbstractUserRepository


class ExampleRepository(AbstractUserRepository):
    """
    Stores users in a SQLite database.
    Defaults to an in-memory database, so data is lost when the app closes.
    Pass a file path (e.g. "db.sqlite3") to keep data between runs.
    """

    def __init__(self, db_path: str = ":memory:"):
        super().__init__()
        # One connection for the lifetime of the repo; an in-memory database
        # only exists as long as its connection is open.
        self._conn = sqlite3.connect(db_path)
        self._conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self) -> None:
        """Creates the users table if it doesn't exist yet"""
        with self._conn:
            self._conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id            TEXT PRIMARY KEY,
                    name          TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL,
                    role          TEXT NOT NULL
                )
                """
            )

    @staticmethod
    def _to_user(row: sqlite3.Row | None) -> User | None:
        """Converts a database row back into a User"""
        if row is None:
            return None
        user = User(name=row["name"], passwordHash=row["password_hash"], role=row["role"])
        # id isn't an init argument, so restore the stored one over the generated one
        user.id = row["id"]
        return user

    def add(self, user: User) -> None:
        """Adds a new user. Raises sqlite3.IntegrityError if the id or name is taken."""
        # Parameterized queries (the ?s) prevent SQL injection
        with self._conn:
            self._conn.execute(
                "INSERT INTO users (id, name, password_hash, role) VALUES (?, ?, ?, ?)",
                (user.id, user.name, user.passwordHash, user.role),
            )

    def get(self, user_id: int) -> User | None:
        """Get's a user by ID"""
        row = self._conn.execute(
            "SELECT id, name, password_hash, role FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()
        return self._to_user(row)

    def get_by_username(self, username: str) -> User | None:
        """Get's a user by their username"""
        row = self._conn.execute(
            "SELECT id, name, password_hash, role FROM users WHERE name = ?",
            (username,),
        ).fetchone()
        return self._to_user(row)

    def get_all(self) -> list[User]:
        """Gets every user, ordered by name"""
        rows = self._conn.execute(
            "SELECT id, name, password_hash, role FROM users ORDER BY name"
        ).fetchall()
        return [self._to_user(row) for row in rows]

    def close(self) -> None:
        """Closes the database connection"""
        self._conn.close()

"""
Module name: auth_service.py
Description: Authentication 
Author: Carson Fujita
Date: 2026-10-13
Version: 0.0.1
"""
import bcrypt

from repository.abstract.abstract_user_repository import AbstractUserRepository

# Used when the username doesn't exist, so the response time doesn't reveal it
_DUMMY_HASH = bcrypt.hashpw(b"dummy-password", bcrypt.gensalt())

# bcrypt only reads the first 72 bytes of a password
_MAX_PASSWORD_BYTES = 72

class AuthService:

    def __init__(self, users: AbstractUserRepository, session):
        self.users = users
        self.session = session

    @staticmethod
    def hash_password(plaintext_password: str) -> str:
        """hashing a password with salt"""
        password = plaintext_password.encode("utf-8")
        if len(password) > _MAX_PASSWORD_BYTES:
            raise ValueError("Password too long")
        return bcrypt.hashpw(password, bcrypt.gensalt()).decode("utf-8")

    @staticmethod
    def verify_password(plaintext_password: str, hashed_password: str) -> bool:
        """Checks creditionals against the stored hash"""
        password = plaintext_password.encode("utf-8")
        if len(password) > _MAX_PASSWORD_BYTES:
            return False
        return bcrypt.checkpw(password, hashed_password.encode("utf-8"))
    
    def login(self, username: str, password: str) -> bool:
        user = self.users.get_by_username(username)

        # prevents guessing if password valid by waittime
        stored_hash = user.passwordHash if user else _DUMMY_HASH.decode("utf-8")

        # Always run bcrypt so a missing user takes as long as a wrong password
        password_ok = AuthService.verify_password(password, stored_hash)
        if user is None or not password_ok:
            return False

        self.session.clear()  # prevent session fixation
        self.session["user_id"] = user.id
        self.session["role"] = user.role
        return True

    def logout(self) -> None:
        self.session.clear()
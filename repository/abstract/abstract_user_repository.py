"""
Module name: abstract_user_repository.py
Description: The user (contract)
Author: Carson Fujita
Date: 2026-10-13
Version: 0.0.1
"""
from abc import ABC, abstractmethod

from model.user import User


class AbstractUserRepository(ABC):        

    @abstractmethod
    def add(self, user: User) -> None:
        """Adds a new user"""

    @abstractmethod
    def get(self, user_id: int) -> User | None:
        """Get's a user by ID"""

    @abstractmethod
    def get_by_username(self, username: str) -> User | None:
        """Get's a user by their username"""

    @abstractmethod
    def get_all(self) -> list[User]:
        """Gets every user"""

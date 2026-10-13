"""
Module name: user.py
Description: The user model
Author: Carson Fujita
Date: 2026-10-13
Version: 0.0.1
"""
import uuid
from dataclasses import dataclass, field


@dataclass
class User:
    """
    Basic user model
    """
    id: int = field(init=False, default_factory=lambda: str(uuid.uuid4()))
    name: str
    passwordHash: str

    """ e.g. Admin, surgeon """
    role: str 
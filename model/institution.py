"""
Module name: institution.py
Description: The Domain Model of the insitution.
Author: Carson Fujita
Date: 2026-10-13
Version: 0.0.1
"""
import uuid
from dataclasses import dataclass, field


@dataclass
class Institution:
    """
    Institution model for every Insitution
    """

    # Generate a UUID for every new instituion; very small chance of overlap.
    id: int = field(init=False, default_factory=lambda: str(uuid.uuid4()))
    name: str

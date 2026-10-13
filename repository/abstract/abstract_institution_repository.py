"""
Module name: abstract_institution_repository.py
Description: The abstract repo (The Contract)
Author: Carson Fujita
Date: 2026-10-13
Version: 0.0.1
"""
from abc import ABC, abstractmethod
from typing import list

from model.institution import Institution


class AbstractInstitutionRepository(ABC):

    @abstractmethod
    def add(self, institution: Institution) -> None:
        pass

    @abstractmethod
    def get(self, institution_id: int) -> Institution | None:
        pass

    @abstractmethod
    def list(self) -> list[Institution]:
        pass
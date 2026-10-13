"""
Module name: decorators.py
Description: Authentication decorators
Author: Carson Fujita
Date: 2026-10-13
Version: 0.0.1
"""

from functools import wraps


def is_logged_in(func):
    """Determines if logged in"""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if "user_id" not in self.controller.auth.session:
            self.controller.show_frame("LoginPage")
            return None
        return func(self, *args, **kwargs)
    return wrapper

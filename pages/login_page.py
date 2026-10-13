"""
module: login_page.py
description: The Example Login page for the application
author: Carson Fujita
date: 2026-10-11
version: 0.0.1
"""

import tkinter as tk


class LoginPage(tk.Frame):
    """
    Class to create the login page for the application.
    Asks for a username and password and logs in through the controller's AuthService.
    """

    def __init__(self, parent, controller):
        """
        Constructor for the LoginPage class
        """
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Login", font=("Arial", 24))
        label.pack(pady=10, padx=10)

        # Grid the fields inside their own frame so the labels and entries line up
        form = tk.Frame(self)
        form.pack(pady=10)

        tk.Label(form, text="Username").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self._entry_username = tk.Entry(form)
        self._entry_username.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form, text="Password").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        # show="*" hides the password as it's typed
        self._entry_password = tk.Entry(form, show="*")
        self._entry_password.grid(row=1, column=1, padx=5, pady=5)

        # Empty until a login fails
        self._label_error = tk.Label(self, text="", fg="red")
        self._label_error.pack()

        button_login = tk.Button(self, text="Login", command=self.login)
        button_login.pack(pady=5)

        button_back = tk.Button(self, text="Back to Main Menu",
                                command=lambda: controller.show_frame("Index"))
        button_back.pack(pady=5)

        # Pressing Enter in either field also logs in
        self._entry_username.bind("<Return>", lambda _event: self.login())
        self._entry_password.bind("<Return>", lambda _event: self.login())

    def login(self) -> None:
        """
        Method to log in with the entered username and password
        """
        username = self._entry_username.get()
        password = self._entry_password.get()

        # Never leave the password sitting in the field
        self._entry_password.delete(0, tk.END)

        if not self.controller.auth.login(username, password):
            # Same message for a wrong username or password, so it doesn't reveal which usernames exist
            self._label_error.config(text="Invalid username or password")
            return

        self._label_error.config(text="")
        self._entry_username.delete(0, tk.END)
        self.controller.show_frame("Index")

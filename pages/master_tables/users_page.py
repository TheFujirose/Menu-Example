"""
Module name: users_page.py
Description: Page for managing users
Author: Carson Fujita
Date: 2026-10-13
Version: 0.2.0
"""
import tkinter as tk
from tkinter import ttk


class UsersPage(tk.Frame):
    """
    Class to create the users page for the application.
    Shows every user in a table, which is reloaded each time the page is shown.
    """

    def __init__(self, parent, controller):
        """
        Constructor for the UsersPage class
        """
        super().__init__(parent)
        self.parent = parent
        self.controller = controller

        # Create a label for the page
        label = tk.Label(self, text="Users", font=("Arial", 24))
        label.pack(pady=10, padx=10)

        # Create a button to go back to the main menu
        # Packed to the bottom before the table so the table can't push it off screen
        button = tk.Button(self, text="Back to Main Menu",
                           command=lambda: controller.show_frame("Index"))
        button.pack(side="bottom", pady=10)

        # Table of users with a scrollbar
        table_frame = tk.Frame(self)
        table_frame.pack(fill="both", expand=True, padx=10)

        # Password hashes are left out on purpose; never show them
        self._table = ttk.Treeview(table_frame, columns=("name", "role", "id"), show="headings")
        self._table.heading("name", text="Name")
        self._table.heading("role", text="Role")
        self._table.heading("id", text="ID")
        self._table.column("id", width=280)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self._table.yview)
        self._table.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self._table.pack(side="left", fill="both", expand=True)

        # controller.show_frame sends this event, so the list is current whenever the page opens
        self.bind("<<ShowFrame>>", lambda _event: self.refresh())

    def refresh(self) -> None:
        """
        Method to reload the table from the user repository
        """
        self._table.delete(*self._table.get_children())
        for user in self.controller.auth.users.get_all():
            self._table.insert("", tk.END, values=(user.name, user.role, user.id))

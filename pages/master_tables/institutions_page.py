"""
Module name: institutions_page.py
Description: Page for managing institutions tables
Author: Carson Fujita
Date: 2026-10-13
Version: 0.1.0
"""
import tkinter as tk


class InstitutionsPage(tk.Frame):
    """
    Class to create the institutions page for the application.
    This class is a subclass of tk.Frame and is used to create the institutions page for the application.
    """

    def __init__(self, parent, controller):
        """
        Constructor for the InstitutionsPage class
        """
        super().__init__(parent)
        self.parent = parent
        self.controller = controller

        # Create a label for the page
        label = tk.Label(self, text="Institutions Page", font=("Arial", 24))
        label.pack(pady=10, padx=10)

        # Create a button to go back to the main menu
        button = tk.Button(self, text="Back to Main Menu",
                           command=lambda: controller.show_frame("Index"))
        button.pack()
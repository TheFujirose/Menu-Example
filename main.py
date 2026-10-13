#!/usr/bin/env python3

"""
Module Name: main.py
Description: Main module for the menu example application
Author: Carson Fujita
Date: 2026-10-11
Version: 0.0.1
"""

import tkinter as tk
import sys

from model.user import User
from pages import example_page, index, login_page
from pages.master_tables import areas_page, institutions_page, users_page
from repository.examples.example_repository import ExampleRepository
from service.auth_service import AuthService


class Main(tk.Tk):
    """
    Main class for the menu example application
    This class is a subclass of tk.Tk and is used to create the main window for the application.
    It initializes the application, sets up the window properties, and manages the different pages of the application.
    """

    _auth: AuthService

    def __init__(self, is_debug: bool):
        """
        Main function to run the application

        Arguement:
            is_debug: sets a user (admin, admin) for debugging
        """
        super().__init__()
        # Authentication service with no current session
        # TODO: You should change the example to your own implementation
        if(is_debug):
            self.auth = AuthService(ExampleRepository(), {})
            self.auth.users.add(User(name="admin", passwordHash=AuthService.hash_password("admin"), role="Admin"))
        else:
            print("WIP, no real database")
            sys.exit(1)

        self.title("Menu Example Application")
        self.geometry("800x600")  # Set the window size
        self.iconphoto(True, tk.PhotoImage(file='assets/icon.png'))  # Set the window icon

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Dictionary to store active page frames
        self.frames = {}
        # Dictionaries have constant time complexity for lookups, so this is a good choice for storing the frames.

        # Initialize and overlay all pages in the same grid spot
        # Linear time complexity for this loop, but it's only run once at the start of the application, so it's not a big deal.
        for PageClass in (index.Index, example_page.ExamplePage, login_page.LoginPage, users_page.UsersPage, areas_page.AreasPage, institutions_page.InstitutionsPage):
            page_name = PageClass.__name__
            # set the controller to self so that the pages can call show_frame
            frame = PageClass(parent=container, controller=self)
            self.frames[page_name] = frame
            
            # Stacking frames directly on top of each other
            frame.grid(row=0, column=0, sticky="nsew")


      
        # Show the initial home screen
        self.show_frame("Index")

    def _construct_menubar(self) -> None:
        """
        Optional method to construct a menubar for the application. 
        This is not currently used, but could be useful in the future.
        to add it, envoke this method in the constructor after the frames are created.
        """
        # build menu bar
        Menubar = tk.Menu(self)
        self.config(menu=Menubar)
        master_tables_menu = tk.Menu(Menubar, tearoff=0)
        master_tables_menu.add_command(label="Institutions", command=self.frames["Index"].view_institutions)
        master_tables_menu.add_command(label="Areas", command=self.frames["Index"].view_areas)
        master_tables_menu.add_command(label="Patients", command=self.frames["Index"].view_patients)

        Menubar.add_cascade(label="Master Tables", menu=master_tables_menu)
        Menubar.add_command(label="Transactions", command=self.frames["Index"].create_procedure)
        Menubar.add_command(label="Reports", command=self.frames["Index"].view_patients_report)
        Menubar.add_command(label="Users", command=self.frames["Index"].view_users_report)
        Menubar.add_command(label="Procedures", command=self.frames["Index"].view_procedures_report)

    def show_frame(self, page_name: str) -> None:
        """
        Show a frame for the given page name
        """
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    # Check for arguements
    arguement_length = len(sys.argv)
    if (arguement_length < 1 or arguement_length > 2):
        print("Usage: python3 main.py <debug?>")
        sys.exit(1)
    elif arguement_length == 1:
        is_debug = False
    else:
        is_debug = bool(sys.argv[1])
    
    app = Main(is_debug)
    app.mainloop()
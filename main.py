#!/usr/bin/env python3

"""
Module Name: main.py
Description: Main module for the menu example application
Author: Carson Fujita
Date: 2026-10-11
Version: 0.0.3
"""

import sys
import tkinter as tk

import config_manager
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

    auth: AuthService

    def __init__(self):
        """
        Main function to run the application
        """
        super().__init__()
        config_manager.readConfigs("configs/client.json")

        if(config_manager.CONFIGS["debug"]):
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

        if(config_manager.CONFIGS["menubar"]):
            self._construct_menubar()
            
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
        self._menubar = tk.Menu(self)
        self.config(menu=self._menubar)        
        # Keep Login/Logout as the last entry so update_menubar can find it with "end"
        self._menubar.add_command(label="Login")
        self.update_menubar()

    def logout(self) -> None:
        self.auth.logout()
        self.update_menubar()
        self.show_frame("Index")

    def update_menubar(self) -> None:
        """Shows Login when logged out and Logout when logged in"""
        if self._menubar is None: # Menubar is optional
            return 
        if "user_id" in self.auth.session:
            self._menubar.entryconfigure("end", label="Logout", command=self.logout)
        else:
            self._menubar.entryconfigure("end", label="Login",
                                         command=lambda: self.show_frame("LoginPage"))


    def show_frame(self, page_name: str) -> None:
        """
        Show a frame for the given page name
        """
        frame = self.frames[page_name]
        frame.tkraise()
        # Lets a page reload its data each time it's shown by binding "<<ShowFrame>>"
        frame.event_generate("<<ShowFrame>>")

if __name__ == "__main__":
    # Check for arguements
    app = Main()
    app.mainloop()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module Name: main.py
Description: Main module for the menu example application
Author: Carson Fujita
Date: 2026-10-11
Version: 0.0.1
"""

import tkinter as tk
from tkinter import ttk
from pages import different_example_page, example_page
from typing import Final
import pages.menu_principal as menu_principal

class Main(tk.Tk):

    def __init__(self):
        """
        Main function to run the application
        """
        super().__init__()
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
        for PageClass in (menu_principal.MenuPrincipal, example_page.ExamplePage, different_example_page.DifferentExamplePage):
            page_name = PageClass.__name__
            # set the controller to self so that the pages can call show_frame
            frame = PageClass(parent=container, controller=self)
            self.frames[page_name] = frame
            
            # Stacking frames directly on top of each other
            frame.grid(row=0, column=0, sticky="nsew")


      
        # Show the initial home screen
        self.show_frame("MenuPrincipal")

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
        master_tables_menu.add_command(label="Institutions", command=self.frames["MenuPrincipal"].view_institutions)
        master_tables_menu.add_command(label="Areas", command=self.frames["MenuPrincipal"].view_areas)
        master_tables_menu.add_command(label="Patients", command=self.frames["MenuPrincipal"].view_patients)

        Menubar.add_cascade(label="Master Tables", menu=master_tables_menu)
        Menubar.add_command(label="Transactions", command=self.frames["MenuPrincipal"].create_procedure)
        Menubar.add_command(label="Reports", command=self.frames["MenuPrincipal"].view_patients_report)
        Menubar.add_command(label="Users", command=self.frames["MenuPrincipal"].view_users_report)
        Menubar.add_command(label="Procedures", command=self.frames["MenuPrincipal"].view_procedures_report)

    def show_frame(self, page_name: str) -> None:
        """
        Show a frame for the given page name
        """
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    app = Main()
    app.mainloop()
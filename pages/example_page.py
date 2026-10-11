"""
module: example_page.py
description: Example page for the application
author: Carson Fujita
date: 2026-10-11
version: 0.0.1
"""

import tkinter as tk

class ExamplePage(tk.Frame):

    def __init__(self, parent, controller):
        """
        Constructor for the ExamplePage class
        """
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="This is an example page")
        label.pack(pady=10, padx=10)

        button = tk.Button(self, text="Go to Home Page",
                           command=lambda: controller.show_frame("MenuPrincipal"))
        button.pack()
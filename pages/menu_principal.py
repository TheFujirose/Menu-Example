"""
Module name: menu.py
Description: Principal menu for app
Author: Carson Fujita
Date: 2026-10-11
Version: 0.0.1
"""
from abc import abstractmethod # Remove this when implementing all methods
import tkinter as tk
from tkinter import Menu

class MenuPrincipal(tk.Frame):
    """
    Class to create the principal menu for the application.
    This class is a subclass of tk.Frame and is used to create the main menu for the application.
    """
    # optional menubar for the application
    _menubar: Menu

    # frames for each section of the menu
    _frame_master_tables: tk.Frame
    _frame_transactions: tk.Frame
    _frame_reports: tk.Frame


    # Variables for the buttons in each section of the menu
    _button_institutions: tk.Button
    _button_areas: tk.Button
    _button_patients: tk.Button
    _button_users: tk.Button

    _button_create_procedure: tk.Button
    _button_update_procedure: tk.Button
    _button_delete_procedure: tk.Button

    _button_patients_report: tk.Button
    _button_users_report: tk.Button
    _button_procedures_report: tk.Button


    def __init__(self, parent, controller):
        """
        Constructor for the MenuPrincipal class
        """
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        
        # Construct the menu sections
        # I put this in a separate method to keep the constructor clean
        self._construct_master_tables_menu()
        self._construct_transactions_menu()
        self._construct_reports_menu()

        # Pack the frames to the root window
        self._frame_master_tables.pack(padx=10, pady=10)
        self._frame_transactions.pack(padx=10, pady=10)
        self._frame_reports.pack(padx=10, pady=10)

    def _construct_master_tables_menu(self) -> None:
        """
        Method to construct the master tables menu
        """
        self._frame_master_tables = tk.Frame(self)
        self._button_institutions = tk.Button(self._frame_master_tables, text="Institutions", command=self.view_institutions)
        self._button_areas = tk.Button(self._frame_master_tables, text="Areas", command=self.view_areas)
        self._button_patients = tk.Button(self._frame_master_tables, text="Patients", command=self.view_patients)
        self._button_users = tk.Button(self._frame_master_tables, text="Users", command=self.view_users)
        self._label_master_tables = tk.Label(self._frame_master_tables, text="Master Tables")
        self._label_master_tables.pack(padx=5, pady=5)
        self._button_institutions.pack(padx=5, pady=5)
        self._button_areas.pack(padx=5, pady=5)
        self._button_patients.pack(padx=5, pady=5)
        self._button_users.pack(padx=5, pady=5)
        pass

    def _construct_transactions_menu(self):
        """
        Method to construct the transactions menu
        """
        self._frame_transactions = tk.Frame(self)
        self._button_create_procedure = tk.Button(self._frame_transactions, text="Create Procedure", command=self.create_procedure)
        self._button_update_procedure = tk.Button(self._frame_transactions, text="Update Procedure", command=self.update_procedure)
        self._button_delete_procedure = tk.Button(self._frame_transactions, text="Delete Procedure", command=self.delete_procedure)
        self._label_transactions = tk.Label(self._frame_transactions, text="Transactions")
        self._label_transactions.pack(padx=5, pady=5)
        self._button_create_procedure.pack(padx=5, pady=5)
        self._button_update_procedure.pack(padx=5, pady=5)
        self._button_delete_procedure.pack(padx=5, pady=5)
        pass

    def _construct_reports_menu(self) -> None:
        """
        Method to construct the reports menu
        """
        self._frame_reports = tk.Frame(self)
        self._button_patients_report = tk.Button(self._frame_reports, text="Patients Report", command=self.view_patients_report)
        self._button_users_report = tk.Button(self._frame_reports, text="Users Report", command=self.view_users_report)
        self._button_procedures_report = tk.Button(self._frame_reports, text="Procedures Report", command=self.view_procedures_report)
        self._label_reports = tk.Label(self._frame_reports, text="Reports")
        self._label_reports.pack(padx=5, pady=5)
        self._button_patients_report.pack(padx=5, pady=5)
        self._button_users_report.pack(padx=5, pady=5)
        self._button_procedures_report.pack(padx=5, pady=5)
        pass

    def view_institutions(self) -> None:
        """
        Method to view institutions
        """
        self.controller.show_frame("ExamplePage")
        pass


    """
    TODO: These methods are not to be overridden, they are to be implemented here. 
    I just put that here to show that these methods are required to be implemented.
    This means you gotta remove the "@abstractmethod" decorator and implement the methods here.
    """

    def view_areas(self) -> None:
        self.controller.show_frame("DifferentExamplePage")
        pass

    @abstractmethod
    def view_patients(self) -> None:
        """
        Method to view patients
        """
        pass

    @abstractmethod
    def view_users(self) -> None:
        """
        Method to view users
        """
        pass

    @abstractmethod
    def create_procedure(self) -> None:
        """
        Method to create a procedure
        """
        pass

    @abstractmethod
    def update_procedure(self) -> None:
        """
        Method to update a procedure
        """
        pass

    @abstractmethod
    def delete_procedure(self) -> None:
        """
        Method to delete a procedure
        """
        pass

    @abstractmethod
    def view_patients_report(self) -> None:
        """
        Method to view patients report
        """
        pass

    @abstractmethod
    def view_users_report(self) -> None:
        """
        Method to view users report
        """
        pass

    @abstractmethod
    def view_procedures_report(self) -> None:
        """
        Method to view procedures report
        """
        pass
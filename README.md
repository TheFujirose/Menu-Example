# Menu-Example

Example Menu System using Python 3.14 and Tkinter. This project demonstrates a simple menu system with multiple pages and navigation between them.

To run the application, ensure you have Python 3.14 installed and execute the `main.py` file. The application window will open, allowing you to navigate through different pages using the menu options.

> [!NOTE]
> Various methods in the `menu_principal.py` file are marked as abstract and need to be implemented in the derived classes.

For your own project it is reccomended to change the application icon to your own. You can do this by replacing the `assets/icon.png` file with your desired icon image. Make sure the new icon file is in the same path and has the same name (`icon.png`) for the application to display it correctly.

Since Tkinter is a built-in library in Python, you do not need to install any additional packages to run this application. Just ensure that you have the correct version of Python installed.

All pages are stored in a dictionary in the `MainApplication` class, which allows for easy access and management of the different pages; constant time complexity for lookups. You can add new pages by creating a new class that inherits from `tk.Frame` and implementing the required methods.

# How to Create a Page

To create a page make a new class that inherits from `tk.Frame` and implement the required methods. You can then add this page to the application by modifying the `main.py` file to include your new page in the frame management system.

For example, if you create a new page class called `NewPage`, you would add it to the `MainApplication` class in `main.py` like this:

```python
    ...
     # Initialize and overlay all pages in the same grid spot
        for PageClass in (menu_principal.MenuPrincipal, example_page.ExamplePage, new_page.NewPage):
    ...
```

# How to call a page from another page

To call a page from another page, you can use the `controller` attribute that is passed to each page. This controller is an instance of the main application class and allows you to switch between pages.

> [!WARNING] 
> Make sure to use the name of the class of the page you want to call, not the name of the file. For example, if you have a page class called `NewPage`, you would call it like this:
> ```python
>     ...
>     self.controller.show_frame("NewPage")
>     ...
> ```
# Menu-Example

Example Menu System using Python 3.14 and Tkinter. This project demonstrates a simple menu system with multiple pages and navigation between them.

<img width="981" height="777" alt="index page" src="https://github.com/user-attachments/assets/b3ef19eb-cbba-4c26-9868-f10917235356" />

To run the application, ensure you have Python 3.14 installed, and you'll need `bcrypt` (used to hash passwords). Run by executing the `main.py` file with an argument like "debug"; see below for details. The application window will open, allowing you to navigate through different pages using the menu options.

For your own project it is recommended to change the application icon to your own. You can do this by replacing the `assets/icon.png` file with your desired icon image. Make sure the new icon file is in the same path and has the same name (`icon.png`) for the application to display it correctly.

Tkinter and SQLite are built into Python, so `bcrypt` is the only package you need to install:

```bash
pip install bcrypt
```

All pages are stored in a dictionary in the `Main` class, which allows for easy access and management of the different pages; constant time complexity for lookups. You can add new pages by creating a new class that inherits from `tk.Frame`; see below.

## Project Layout

```
main.py                 # Main window; registers pages and sets up authentication
assets/icon.png         # Window icon
auth/decorators.py      # @is_logged_in decorator for protecting page actions
model/                  # Data classes (User, Institution)
pages/                  # Pages (Index is the home screen, LoginPage, ExamplePage)
pages/master_tables/    # Users, Areas and Institutions pages
repository/abstract/    # Repository contracts you implement
repository/examples/    # ExampleRepository, a SQLite implementation of the user repository
service/auth_service.py # Login, logout, password hashing and the session
```

## How to Create a Page

To create a page make a new class that inherits from `tk.Frame`. Its constructor must take `parent` and `controller` and pass `parent` to `tk.Frame`:

```python
import tkinter as tk


class NewPage(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
```

You can then add this page to the application by importing it in `main.py` and adding it to the loop in the `Main` class.

For example, if you create a new page class called `NewPage` in `pages/new_page.py`, you would add it like this:

```python
from pages import example_page, index, login_page, new_page
...
        # Initialize and overlay all pages in the same grid spot
        for PageClass in (index.Index, example_page.ExamplePage, login_page.LoginPage, ..., new_page.NewPage):
...
```

The first page shown is `Index`, set by `self.show_frame("Index")` at the end of the constructor.

## How to call a page from another page

To call a page from another page, you can use the `controller` attribute that is passed to each page. This controller is an instance of the main application class and allows you to switch between pages.

> [!WARNING] 
> Make sure to use the name of the class of the page you want to call, not the name of the file. For example, if you have a page class called `NewPage`, you would call it like this:
> ```python
>     ...
>     self.controller.show_frame("NewPage")
>     ...
> ```

## Requiring a Login

<img width="997" height="435" alt="login page" src="https://github.com/user-attachments/assets/be7f16c8-ab09-46d3-8abb-7c1175510070" />


Page actions can be protected with the `@is_logged_in` decorator from `auth/decorators.py`. If no one is logged in, the user is sent to `LoginPage` instead of running the method. All the buttons on the `Index` page use it:

```python
from auth.decorators import is_logged_in
...
    @is_logged_in
    def view_users(self) -> None:
        self.controller.show_frame("UsersPage")
```

The decorator expects the page to have a `self.controller`. Login state is kept in `controller.auth.session` (a dictionary holding `user_id` and `role`), which `AuthService.login` fills and `AuthService.logout` clears.

## Linting

We use `ruff` for linting. Install it, then run the linter by executing the following commands in your terminal:

```bash
pip install ruff
ruff check .
```

## Running

Run from the project root, since the icon is loaded from the relative path `assets/icon.png`. On Windows use `python` instead of `python3`.

```bash
python3 main.py debug
```
Above terminal will run in debug mode, which uses an in-memory SQLite database (wiped when the app closes) with one user already added. Log in with:

- Username: `admin`
- Password: `admin`

I recommend you remove this feature in your own version. This is just done because it forces anyone who forks this to remove the line that adds an admin with password admin from their implementation; it's designed to be hard to miss.

Running without an argument (`python3 main.py`) prints "WIP, no real database" and exits, since there is no real database yet. Note that any argument turns on debug mode, not only "debug".

### Repository and Model use

This uses a repository pattern so you'll have to implement your own models and abstracts. Pages and services depend on the abstract classes in `repository/abstract/`, not on a specific database.

For users, subclass `AbstractUserRepository` and implement:

- `add(user)` to save a new user
- `get(user_id)` to find a user by ID, or return `None`
- `get_by_username(username)` to find a user by name, or return `None`

`ExampleRepository` in `repository/examples/` is a working SQLite version. By default it uses an in-memory database; pass a file path (e.g. `ExampleRepository("db.sqlite3")`) to keep data between runs.

To use your own repository, swap it in where `AuthService` is created in `main.py`:

```python
self.auth = AuthService(YourUserRepository(), {})
```

### Optional Menubar

`Main` has an unused `_construct_menubar` method that adds a menu bar with the same actions as the `Index` page. To enable it, call `self._construct_menubar()` in the constructor after the pages are created.

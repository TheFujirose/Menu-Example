# Menu-Example

Example Menu System using Python 3.14 and Tkinter. This project demonstrates a simple menu system with multiple pages and navigation between them.

<img width="981" height="777" alt="image" src="https://github.com/user-attachments/assets/b3ef19eb-cbba-4c26-9868-f10917235356" />

To run the application, ensure you have Python 3.14 installed, and you'll need `bcrypt` (used to hash passwords). Run by executing the `main.py` file; settings such as debug mode are read from `configs/client.json` (see [Configuration](#configuration)). The application window will open, allowing you to navigate through different pages using the menu options.

For your own project it is recommended to change the application icon to your own. You can do this by replacing the `assets/icon.png` file with your desired icon image. Make sure the new icon file is in the same path and has the same name (`icon.png`) for the application to display it correctly.

Tkinter and SQLite are built into Python, so `bcrypt` is the only package you need to install:

```bash
pip install bcrypt
```

All pages are stored in a dictionary in the `Main` class, which allows for easy access and management of the different pages; constant time complexity for lookups. You can add new pages by creating a new class that inherits from `tk.Frame`; see below.

## Project Layout

```
main.py                 # Main window; registers pages and sets up authentication
config_manager.py       # Loads configs/client.json into config_manager.CONFIGS
configs/client.json     # App settings (debug mode, menubar)
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

All pages are created once at startup, so a page that shows data should reload it each time it's opened. `show_frame` sends a `<<ShowFrame>>` event to the page it shows; bind it to a refresh method (see `UsersPage`):

```python
        self.bind("<<ShowFrame>>", lambda _event: self.refresh())
```

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

Page actions can be protected with the `@is_logged_in` decorator from `auth/decorators.py`. If no one is logged in, the user is sent to `LoginPage` instead of running the method. All the buttons on the `Index` page use it:

```python
from auth.decorators import is_logged_in
...
    @is_logged_in
    def view_users(self) -> None:
        self.controller.show_frame("UsersPage")
```

The decorator expects the page to have a `self.controller`. Login state is kept in `controller.auth.session` (a dictionary holding `user_id` and `role`), which `AuthService.login` fills and `AuthService.logout` clears.

To log out, call `controller.logout()` rather than `controller.auth.logout()`; it also updates the menubar and returns to `Index`. If you log a user in somewhere other than `LoginPage`, call `controller.update_menubar()` afterwards so the menubar shows Logout.

## Linting

We use `ruff` for linting. Install it, then run the linter by executing the following commands in your terminal:

```bash
pip install ruff
ruff check .
```

## Running

Run from the project root, since `configs/client.json` and `assets/icon.png` are loaded from relative paths. On Windows use `python` instead of `python3`.

```bash
python3 main.py
```
With `"debug": true` in `configs/client.json` (the default in this repo), the app runs in debug mode, which uses an in-memory SQLite database (wiped when the app closes) with one user already added. Log in with:

- Username: `admin`
- Password: `admin`

I recommend you remove this feature in your own version. This is just done because it forces anyone who forks this to remove the line that adds an admin with password admin from their implementation; it's designed to be hard to miss.

With `"debug": false` the app prints "WIP, no real database" and exits, since there is no real database yet.

## Configuration

Settings are read from `configs/client.json` when the app starts:

```json
{
    "menubar": true,
    "debug": true
}
```

| Key       | Effect |
|-----------|--------|
| `debug`   | `true` uses the in-memory example database with the `admin` user. `false` exits, until you add a real database. |
| `menubar` | `true` shows the menubar (see [Optional Menubar](#optional-menubar)). |

`config_manager.readConfigs` replaces `config_manager.CONFIGS` with the file's contents, so every key must be in the file; a missing key raises a `KeyError`. To read a setting elsewhere, import the module and look it up:

```python
import config_manager
...
if config_manager.CONFIGS["menubar"]:
    ...
```

Use `import config_manager`, not `from config_manager import CONFIGS`; the second form keeps the defaults from before the file was read.

### Repository and Model use

This uses a repository pattern so you'll have to implement your own models and abstracts. Pages and services depend on the abstract classes in `repository/abstract/`, not on a specific database.

For users, subclass `AbstractUserRepository` and implement:

- `add(user)` to save a new user
- `get(user_id)` to find a user by ID, or return `None`
- `get_by_username(username)` to find a user by name, or return `None`
- `get_all()` to return every user (used by the Users page)

`ExampleRepository` in `repository/examples/` is a working SQLite version. By default it uses an in-memory database; pass a file path (e.g. `ExampleRepository("db.sqlite3")`) to keep data between runs.

To use your own repository, swap it in where `AuthService` is created in `main.py`:

```python
self.auth = AuthService(YourUserRepository(), {})
```

### Optional Menubar

Set `"menubar": true` in `configs/client.json` to show a menubar. It has one entry that shows **Login** when no one is logged in (opens `LoginPage`) and **Logout** when someone is (calls `controller.logout()`). `update_menubar` swaps it, and is called after logging in or out.

To add your own entries, add them in `_construct_menubar` before the Login/Logout entry. Login/Logout must stay last, since `update_menubar` finds it by its `"end"` index:

```python
        self._menubar = tk.Menu(self)
        self.config(menu=self._menubar)
        self._menubar.add_command(label="Users", command=lambda: self.show_frame("UsersPage"))
        # Keep Login/Logout as the last entry so update_menubar can find it with "end"
        self._menubar.add_command(label="Login")
        self.update_menubar()
```

Tk menus can't hide entries. To grey one out while logged out, use `self._menubar.entryconfigure(index, state="disabled")` in `update_menubar`, and `state="normal"` to turn it back on.
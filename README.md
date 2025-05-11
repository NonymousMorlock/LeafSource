# Library CLI

A simple command-line library management application built with Python, Typer, and SQLAlchemy using SQLite for storage. It features authentication with role-based authorization:

* **Librarian**: Can add/remove users and books.
* **Member**: Can borrow and return books.

All actions require authentication.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Project Structure](#project-structure)
4. [Configuration](#configuration)
5. [Initializing the Database](#initializing-the-database)
6. [Authentication Commands](#authentication-commands)
7. [User Management (Librarian Only)](#user-management-librarian-only)
8. [Book Management (Librarian Only)](#book-management-librarian-only)
9. [Borrowing Commands](#borrowing-commands)
10. [Testing](#testing)
11. [Notes](#notes)

---

## Prerequisites

* Python 3.8 or higher
* SQLite (bundled with Python)

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/NonymousMorlock/LeafSource.git
   cd LeafSource
   ```

2. (Optional) Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # on macOS/Linux
   .\.venv\Scripts\activate  # on Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## Project Structure

```bash
LeafSource/
├── config/
│   ├── db.py            # SQLAlchemy engine, session, Base
│   ├── security.py      # Password hashing and verification
│   └── session.py       # CLI session (login state)
├── models/
│   ├── user.py          # User and RoleEnum models
│   ├── book.py          # Book model
│   └── borrow.py        # Borrow record model
├── cli/
│   ├── auth.py          # `login`, `logout`, `whoami`
│   ├── user.py          # `create-user`, `list-users`
│   ├── book.py          # `add-book`, `remove-book`, `list-books`
│   ├── borrow.py        # `borrow-book`, `return-book`, `list-borrows`
│   └── main.py          # Entry point that wires all commands
├── tests/               # (Optional) test suite
└── library.db           # SQLite database file (created after init)
```

---

## Configuration

* **Database URL** is defined in `LeafSource/config/db.py` as `sqlite:///./library.db`.
* **Session file** for tracking logged-in user is `~/.library_cli_session.json`.

---

## Initializing the Database

Before any commands, create the schema:

```bash
python -m LeafSource.cli.main init-db
# or, if installed as package:
library init-db
```

This will create `library.db` with the required tables.

---

## Authentication Commands

| Command               | Description                 |
| --------------------- | --------------------------- |
| `library auth login`  | Log in as existing user     |
| `library auth logout` | Log out current user        |
| `library auth whoami` | Show current logged-in user |

---

## User Management (Librarian Only)

| Command                    | Description       |
| -------------------------- | ----------------- |
| `library user create-user` | Create a new user |
| `library user list-users`  | List all users    |

**Example:**

```bash
library user create-user alice --password secret --role member
library user list-users
```

---

## Book Management (Librarian Only)

| Command                              | Description                          |
| ------------------------------------ | ------------------------------------ |
| `library book add-book`              | Add a book to the catalog            |
| `library book remove-book [BOOK_ID]` | Remove a book by its ID              |
| `library book list-books`            | List available books                 |
| `library book list-books --all`      | List all books including unavailable |

**Example:**

```bash
library book add-book "1984" "George Orwell" 9780451524935 --copies 3
library book list-books
```

---

## Borrowing Commands

| Command                                  | Description                                 |
| ---------------------------------------- | ------------------------------------------- |
| `library borrow borrow-book [BOOK_ID]`   | Borrow a book by its ID (members only)      |
| `library borrow return-book [BORROW_ID]` | Return a borrowed book by record ID         |
| `library borrow list-borrows`            | List active borrow records for current user |
| `library borrow list-borrows --all`      | List all borrow records including returned  |

**Example:**

```bash
library borrow borrow-book 5
library borrow list-borrows
```

---

## Testing

You can add unit tests under the `tests/` directory. To run tests:

```bash
pytest
```

---

## Notes

* All commands require an active login session. Use `library auth login` first.
* The session persists in a file in your home directory.
* To customize settings, edit the modules under `LeafSource/config/`.

Enjoy managing your library from the command line!

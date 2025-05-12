from .auth import auth_app
from .user import user_app
from .book import book_app
from .borrow import borrow_app

__all__ = ["auth_app", "user_app", "book_app", "borrow_app"]

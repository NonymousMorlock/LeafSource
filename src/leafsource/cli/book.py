import typer

from leafsource.cli.auth import require_login
from leafsource.config import SessionLocal
from leafsource.models.book import Book

book_app = typer.Typer(help="Book management commands")


def require_librarian():
    from leafsource.cli.user import require_librarian as rl
    return rl()

@book_app.command()
def add_book(title: str, author: str, isbn: str, copies: int = 1):
    """Add a new book to catalog"""
    require_librarian()
    db = SessionLocal()
    try:
        book = Book(title=title, author=author, isbn=isbn, copies_available=copies)
        db.add(book)
        db.commit()
        typer.secho(f"Added book '{title}' (id={book.id})", fg=typer.colors.GREEN)
    finally:
        db.close()

@book_app.command()
def remove_book(book_id: int):
    """Remove a book by its ID"""
    require_librarian()
    db = SessionLocal()
    try:
        book = db.query(Book).get(book_id)
        if not book:
            typer.secho("Book not found", fg=typer.colors.RED)
            raise typer.Exit(code=1)
        db.delete(book)
        db.commit()
        typer.secho(f"Removed book id={book_id}", fg=typer.colors.YELLOW)
    finally:
        db.close()

@book_app.command()
def list_books(show_all: bool = typer.Option(False, "--all", help="Show even unavailable books")):
    """List available books"""
    require_login()
    db = SessionLocal()
    try:
        query = db.query(Book)
        if not show_all:
            query = query.filter(Book.copies_available > 0)
        books = query.all()
        for b in books:
            typer.echo(f"{b.id}: {b.title} by {b.author} - {b.copies_available} copies available")
    finally:
        db.close()
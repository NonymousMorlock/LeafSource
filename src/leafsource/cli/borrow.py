from datetime import datetime, UTC

import typer

from leafsource.cli.auth import require_login
from leafsource.config import SessionLocal
from leafsource.models.book import Book
from leafsource.models.borrow import Borrow
from leafsource.models.user import RoleEnum

borrow_app = typer.Typer(help="Borrowing commands")


@borrow_app.command()
def borrow_book(book_id: int):
    """Borrow a book by its ID"""
    user = require_login()
    if user.role != RoleEnum.MEMBER:
        typer.secho("Only members can borrow books", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    db = SessionLocal()
    try:
        book = db.query(Book).get(book_id)
        if not book or book.copies_available < 1:
            typer.secho("Book not available", fg=typer.colors.RED)
            raise typer.Exit(code=1)
        book.copies_available -= 1
        borrow = Borrow(user_id=user.id, book_id=book_id)
        db.add(borrow)
        db.commit()
        typer.secho(f"Book '{book.title}' borrowed", fg=typer.colors.GREEN)
    finally:
        db.close()


@borrow_app.command()
def return_book(borrow_id: int):
    """Return a borrowed book by borrow record ID"""
    user = require_login()
    db = SessionLocal()
    try:
        borrow = db.query(Borrow).get(borrow_id)
        if not borrow or borrow.user_id != user.id:
            typer.secho("Borrow record not found or not yours", fg=typer.colors.RED)
            raise typer.Exit(code=1)
        if borrow.returned_at:
            typer.secho("Already returned", fg=typer.colors.YELLOW)
            raise typer.Exit(code=1)
        borrow.returned_at = datetime.now(UTC)
        borrow.book.copies_available += 1
        db.commit()
        typer.secho(f"Book returned successfully", fg=typer.colors.GREEN)
    finally:
        db.close()


@borrow_app.command()
def list_borrows(all: bool = typer.Option(False, "--all", help="Include returned records")):
    """List your borrow records"""
    user = require_login()
    db = SessionLocal()
    try:
        query = db.query(Borrow).filter(Borrow.user_id == user.id)
        if not all:
            query = query.filter(Borrow.returned_at.is_(None))
        records = query.all()
        for br in records:
            status = "Returned" if br.returned_at else "Borrowed"
            typer.echo(f"{br.id}: Book ID {br.book_id} on {br.borrowed_at} - {status}")
    finally:
        db.close()

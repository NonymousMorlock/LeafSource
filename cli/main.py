import typer
from library_app.config.db import engine, Base
from library_app.cli.auth import auth_app
from library_app.cli.user import user_app
from library_app.cli.book import book_app
from library_app.cli.borrow import borrow_app

app = typer.Typer()

app.add_typer(auth_app, name="auth")
app.add_typer(user_app, name="user")
app.add_typer(book_app, name="book")
app.add_typer(borrow_app, name="borrow")

@app.command()
def init_db():
    """Initialize database and create tables"""
    Base.metadata.create_all(bind=engine)
    typer.secho("Database initialized.", fg=typer.colors.GREEN)

if __name__ == "__main__":
    app()
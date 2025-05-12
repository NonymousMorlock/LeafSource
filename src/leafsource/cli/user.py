import typer
from leafsource.cli.auth import require_login
from leafsource.config import SessionLocal
from leafsource.models.user import User, RoleEnum
from leafsource.config import hash_password

user_app = typer.Typer(help="User management (librarian only)")


def require_librarian():
    user = require_login()
    if user.role != RoleEnum.LIBRARIAN:
        typer.secho("Requires librarian role", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    return user

@user_app.command()
def create_user(username: str, password: str, role: RoleEnum = RoleEnum.MEMBER):
    """Create a new user with specified role"""
    require_librarian()
    db = SessionLocal()
    try:
        hashed = hash_password(password)
        new_user = User(username=username, hashed_password=hashed, role=role)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        typer.secho(f"Created user {new_user.username} (id={new_user.id})", fg=typer.colors.GREEN)
    finally:
        db.close()

@user_app.command()
def list_users():
    """List all users"""
    require_librarian()
    db = SessionLocal()
    try:
        users = db.query(User).all()
        for u in users:
            typer.echo(f"{u.id}: {u.username} ({u.role})")
    finally:
        db.close()

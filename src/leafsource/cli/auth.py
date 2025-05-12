import typer
from leafsource.config import login_user, logout_user, get_current_user

auth_app = typer.Typer(help="Authentication commands")


@auth_app.command()
def login(username: str = typer.Option(..., prompt=True),
          password: str = typer.Option(..., prompt=True, hide_input=True)):
    """Log in as an existing user"""
    user = login_user(username, password)
    if not user:
        typer.secho("Invalid credentials", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    typer.secho(f"Logged in as {user.username} ({user.role})", fg=typer.colors.GREEN)


@auth_app.command()
def logout():
    """Log out current user"""
    logout_user()
    typer.secho("Logged out", fg=typer.colors.YELLOW)


def require_login():
    user = get_current_user()
    if not user:
        typer.secho("You must be logged in to perform this action", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    return user

@auth_app.command(name="whoami")
def whoami():
    """Show current logged-in user"""
    user = get_current_user()
    if not user:
        typer.secho("Not logged in", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    typer.echo(f"Username: {user.username}\nRole: {user.role}")
import json
from pathlib import Path

from leafsource.config import SessionLocal
from leafsource.config import verify_password
from leafsource.models.user import User

SESSION_FILE = Path.home() / ".library_cli_session.json"


def login_user(username: str, password: str):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user or not verify_password(password, user.hashed_password):
            return None
        SESSION_FILE.write_text(json.dumps({"user_id": user.id}))
        return user
    finally:
        db.close()


def logout_user():
    if SESSION_FILE.exists():
        SESSION_FILE.unlink()


def get_current_user():
    if not SESSION_FILE.exists():
        return None
    data = json.loads(SESSION_FILE.read_text())
    user_id = data.get("user_id")
    db = SessionLocal()
    try:
        return db.query(User).get(user_id)
    finally:
        db.close()

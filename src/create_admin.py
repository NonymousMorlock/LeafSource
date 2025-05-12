from src.leafsource.config.db import engine, SessionLocal, Base
from src.leafsource.config.security import hash_password
from src.leafsource.models.user import User, RoleEnum

# Make sure tables exist
Base.metadata.create_all(bind=engine)

db = SessionLocal()
admin = User(
    username="username", # Replace this with your one init
    hashed_password=hash_password("password"), # Replace this as well
    role=RoleEnum.LIBRARIAN
)
db.add(admin)
db.commit()
db.close()
print("� First librarian ‘admin’ created. Now run ‘library auth login’.")

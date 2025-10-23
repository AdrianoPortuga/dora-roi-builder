from app.database import SessionLocal, init_db
from app import models
from app.security import hash_password
from app.config import settings

def run():
    init_db()
    db = SessionLocal()
    try:
        org = models.Organization(name="Default Org")
        db.add(org); db.flush()
        user = models.User(org_id=org.id, email=settings.seed_email, password_hash=hash_password(settings.seed_password), role="owner")
        db.add(user)
        db.commit()
        print("Seeded:", settings.seed_email)
    finally:
        db.close()

if __name__ == "__main__":
    run()

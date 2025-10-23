from passlib.hash import argon2
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal
from app.models.base import Base
from app.models.organization import Organization
from app.models.user import User

def run():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    try:
        org = Organization(name="Org Demo")
        db.add(org)
        db.flush()
        user = User(
            organization_id=org.id,
            email="admin@demo.com",
            full_name="Admin Demo",
            password_hash=argon2.hash("demo123"),
            is_active=True,
        )
        db.add(user)
        db.commit()
        print("Seed ok. Login: admin@demo.com / senha: demo123")
    finally:
        db.close()

if __name__ == "__main__":
    run()

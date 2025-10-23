from app.database import engine
from sqlalchemy import text
from passlib.hash import pbkdf2_sha256

EMAIL = "admin@demo.com"
NEW_PLAIN = "admin"

new_hash = pbkdf2_sha256.hash(NEW_PLAIN)

with engine.begin() as conn:
    res = conn.execute(text("UPDATE [user] SET password_hash=:ph WHERE email=:em"),
                       {"ph": new_hash, "em": EMAIL})
    print(f"Linhas afetadas: {res.rowcount}")

# conferência
with engine.connect() as conn:
    row = conn.execute(text("SELECT email, password_hash FROM [user] WHERE email=:em"),
                       {"em": EMAIL}).mappings().first()
    print("Email:", row["email"])
    print("Hash prefix:", row["password_hash"][:20], "...")

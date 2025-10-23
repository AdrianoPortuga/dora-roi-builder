from app.database import engine
from sqlalchemy import text
from passlib.hash import pbkdf2_sha256

EMAIL = "admin@demo.com"
PLAIN = "admin"

with engine.connect() as conn:
    row = conn.execute(text("SELECT email, password_hash, is_active FROM [user] WHERE email=:em"), {"em": EMAIL}).mappings().first()
    if not row:
        print("NÃO ENCONTREI admin@demo.com")
    else:
        print("email:", row["email"], "is_active:", row["is_active"])
        ok = False
        try:
            ok = pbkdf2_sha256.verify(PLAIN, row["password_hash"])
        except Exception as e:
            print("erro verify:", e)
        print("senha 'admin' confere?:", ok)

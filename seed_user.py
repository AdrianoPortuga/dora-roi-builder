from passlib.hash import pbkdf2_sha256
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal
from app.models.base import Base
from app.models.organization import Organization
from app.models.user import User
from app.models.role import Role, RolePermission, UserRole

ADMIN_PERMS = [
    "vendors:read", "vendors:write",
    "risks:read", "risks:write",
    "controls:read", "controls:write",
    "audit:read", "users:admin",
]

VIEWER_PERMS = [
    "vendors:read"
]

def upsert_role(db: Session, org_id: int, name: str, perms: list[str]) -> Role:
    role = db.query(Role).filter(Role.organization_id==org_id, Role.name==name).first()
    if not role:
        role = Role(organization_id=org_id, name=name)
        db.add(role); db.flush()
    # sincroniza permissÃµes
    existing = {rp.permission for rp in db.query(RolePermission).filter(RolePermission.role_id==role.id).all()}
    for p in perms:
        if p not in existing:
            db.add(RolePermission(role_id=role.id, permission=p))
    db.commit()
    return role

def ensure_user_role(db: Session, user_id: int, role_id: int):
    link = db.query(UserRole).filter(UserRole.user_id==user_id, UserRole.role_id==role_id).first()
    if not link:
        db.add(UserRole(user_id=user_id, role_id=role_id))
        db.commit()

def run():
    print(">> Creating tables...")
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    try:
        org = db.query(Organization).filter(Organization.name=="Org Demo").first()
        if not org:
            org = Organization(name="Org Demo")
            db.add(org); db.flush()
            print(f">> Created org id={org.id}")

        admin = db.query(User).filter(User.email=="admin@demo.com").first()
        if not admin:
            admin = User(
                organization_id=org.id, email="admin@demo.com",
                full_name="Admin Demo",
                password_hash=pbkdf2_sha256.hash("demo123"),
                is_active=True
            )
            db.add(admin); db.commit()
            print(">> Created admin user")
        else:
            admin.password_hash = pbkdf2_sha256.hash("demo123")
            admin.organization_id = org.id
            admin.is_active = True
            db.commit()
            print(">> Updated admin password (PBKDF2)")

        # cria papÃ©is e vincula
        admin_role = upsert_role(db, org.id, "admin", ADMIN_PERMS)
        viewer_role = upsert_role(db, org.id, "viewer", VIEWER_PERMS)
        ensure_user_role(db, admin.id, admin_role.id)

        # um usuÃ¡rio viewer para testar 403
        viewer = db.query(User).filter(User.email=="viewer@demo.com").first()
        if not viewer:
            viewer = User(
                organization_id=org.id, email="viewer@demo.com",
                full_name="Viewer Demo",
                password_hash=pbkdf2_sha256.hash("viewer123"),
                is_active=True
            )
            db.add(viewer); db.commit()
            print(">> Created viewer user")
        ensure_user_role(db, viewer.id, viewer_role.id)

        print("Seed ok. Admin: admin@demo.com/demo123 | Viewer: viewer@demo.com/viewer123")
    finally:
        db.close()

if __name__ == "__main__":
    run()

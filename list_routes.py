from app.main import app
print("\n=== Rotas registradas ===")
for r in app.routes:
    methods = ",".join(sorted(getattr(r, "methods", []) or []))
    print(f"{methods:20s}  {r.path}")

from app.database import engine
from sqlalchemy import inspect, text

print('== Tabelas ==')
i = inspect(engine)
print(i.get_table_names())

candidates = ['users','user','app_user','account','accounts','auth_user']
found_any = False

with engine.connect() as conn:
    for t in candidates:
        try:
            rows = conn.execute(text(f'SELECT * FROM {t} LIMIT 5')).mappings().all()
            if rows:
                print(f'\n== Conteúdo de {t} (até 5 linhas) ==')
                for r in rows:
                    d = dict(r)
                    print({k: d.get(k) for k in list(d.keys())[:10]})
                found_any = True
        except Exception as e:
            pass

if not found_any:
    print('\n(Não achei usuários nas tabelas candidatas. Pode não existir usuário seed.)')

// src/components/Header.tsx
import { useEffect, useState } from 'react';
import { getHealth, Health } from '../services/system';

export default function Header() {
  const [health, setHealth] = useState<Health | null>(null);

  useEffect(() => {
    getHealth().then(setHealth).catch(() => setHealth(null));
  }, []);

  const ok = health?.status === 'ok';

  return (
    <header style={{
      display: 'flex', alignItems: 'center', justifyContent: 'space-between',
      padding: '12px 16px', borderBottom: '1px solid #222', background: '#0b1220', color: '#eaeef5'
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
        <div style={{ width: 10, height: 10, borderRadius: '50%', background: ok ? '#22c55e' : '#ef4444' }} />
        <strong>DORA RoI Builder</strong>
        <span style={{
          fontSize: 12, padding: '4px 8px', borderRadius: 999, background: '#111827', border: '1px solid #1f2937'
        }}>
          API {health?.version ?? 'â€“'} ({health?.env ?? 'â€“'})
        </span>
      </div>

      <div style={{ fontSize: 12, opacity: 0.8 }}>
        usuÃ¡rio: admin@demo.com
      </div>
    </header>
  );
}

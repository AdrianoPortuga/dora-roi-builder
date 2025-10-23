import { useEffect, useState } from "react";
import api from "../api/client";

export default function Vendors() {
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState("");

  async function load() {
    try {
      setErr("");
      setLoading(true);
      const { data } = await api.get("/"); // GET /api/v1/
      setRows(data || []);
    } catch (e) {
      console.error(e);
      setErr("Falha ao carregar vendors");
    } finally {
      setLoading(false);
    }
  }

  async function createVendor(payload) {
    await api.post("/", payload); // POST /api/v1/
    await load();
  }

  useEffect(() => { load(); }, []);

  return (
    <div className="p-6 text-white">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl">Vendors</h2>
        <button
          onClick={() => createVendor({ name: "Farmacia UI", country: "BR", criticality: "low" })}
          className="px-4 py-2 bg-blue-600 rounded"
        >
          Novo Vendor (demo)
        </button>
      </div>
      {err && <div className="text-red-400 mb-3">{err}</div>}
      {loading ? (
        <div>Carregando…</div>
      ) : (
        <table className="w-full text-left">
          <thead><tr><th>ID</th><th>Nome</th><th>País</th><th>Criticidade</th></tr></thead>
          <tbody>
            {rows.map(r => (
              <tr key={r.id}>
                <td>{r.id}</td><td>{r.name}</td><td>{r.country}</td><td>{r.criticality}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

import { useEffect, useState } from "react";
import api from "../api/client";
import Button from "../components/ui/Button";
import Input, { Label } from "../components/ui/Input";
import Select from "../components/ui/Select";
import Card from "../components/ui/Card";
import { Table, THead, Tr, Th, TBody, Td } from "../components/ui/Table";
import ConfirmDialog from "../components/ConfirmDialog";
import { useToast } from "../components/ToastProvider";

export default function Vendors() {
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);
  const [form, setForm] = useState({ name: "", country: "PT", criticality: "low" });

  // edição inline
  const [editingId, setEditingId] = useState(null);
  const [editForm, setEditForm] = useState({ name: "", country: "", criticality: "low" });
  const [rowAction, setRowAction] = useState(null); // id em ação (salvar/deletar)
  const [confirmDlg, setConfirmDlg] = useState({ open: false, id: null, name: "" });
  const { addToast } = useToast();

  async function load() {
    setLoading(true);
    setError("");
    try {
      const data = await api.listVendors();
      setRows(data);
    } catch (err) {
      if (err?.response?.status === 401) {
        window.location.href = "/";
      } else {
        setError("Erro ao carregar vendors");
        console.error(err);
      }
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { load(); }, []);

  async function onCreate(e) {
    e.preventDefault();
    if (!form.name.trim()) return;
    setSaving(true);
    try {
      const created = await api.createVendor(form);
      setRows((prev) => [created, ...prev]);
      setForm({ name: "", country: "PT", criticality: "low" });
      addToast({ type: "success", message: "Vendor criado" });
    } catch (err) {
      if (err?.response?.status === 401) {
        window.location.href = "/";
      } else {
        alert("Falha ao criar vendor");
        console.error(err);
      }
    } finally {
      setSaving(false);
    }
  }

  function startEdit(v) {
    const rowEl = document.querySelector(`[data-row="vendor-${v.id}"]`);
    if (rowEl && rowEl.scrollIntoView) {
      rowEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
    setEditingId(v.id);
    setEditForm({ name: v.name || "", country: v.country || "", criticality: v.criticality || "low" });
    setTimeout(() => { document.getElementById('e-name')?.focus(); }, 50);
  }

  function cancelEdit() {
    setEditingId(null);
  }

  async function saveEdit(id) {
    setRowAction(id);
    try {
      const updated = await api.updateVendor(id, editForm);
      setRows((prev) => prev.map((r) => (r.id === id ? updated : r)));
      setEditingId(null);
      addToast({ type: "success", message: "Alterações salvas" });
    } catch (err) {
      console.error(err);
      addToast({ type: "error", message: "Falha ao salvar" });
    } finally {
      setRowAction(null);
    }
  }

  async function removeConfirmed(id) {
    setRowAction(id);
    try {
      await api.deleteVendor(id);
      setRows((prev) => prev.filter((r) => r.id !== id));
      addToast({ type: "success", message: "Vendor removido" });
    } catch (err) {
      console.error(err);
      addToast({ type: "error", message: "Falha ao remover" });
    } finally {
      setRowAction(null);
      setConfirmDlg({ open: false, id: null, name: "" });
    }
  }

  const inputCls = ""; // classes já embutidas nos componentes

  if (error) {
    return (
      <div className="max-w-4xl mx-auto p-4">
        <div className="bg-red-900/30 border border-red-700 text-red-200 px-4 py-3 rounded-lg">
          {error}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Vendors</h1>
          <p className="text-sm text-slate-300">Cadastro e gestão de fornecedores</p>
        </div>
        <Button variant="secondary" onClick={load} disabled={loading}>
          {loading ? "Atualizando..." : "Atualizar"}
        </Button>
      </div>

      <Card>
        <form onSubmit={onCreate} className="grid grid-cols-1 gap-3 sm:grid-cols-12">
          <div className="sm:col-span-6">
            <Label htmlFor="name">Nome do fornecedor</Label>
            <Input id="name" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} placeholder="Ex.: NovaCo" required />
          </div>
          <div className="sm:col-span-2">
            <Label htmlFor="country">País</Label>
            <Input id="country" value={form.country} onChange={(e) => setForm({ ...form, country: e.target.value })} placeholder="PT, BR" />
          </div>
          <div className="sm:col-span-2">
            <Label htmlFor="criticality">Criticidade</Label>
            <Select id="criticality" value={form.criticality} onChange={(e) => setForm({ ...form, criticality: e.target.value })}>
              <option value="low">low</option>
              <option value="medium">medium</option>
              <option value="high">high</option>
            </Select>
          </div>
          <div className="sm:col-span-2 flex items-end">
            <Button type="submit" className="w-full" loading={saving}>
              {saving ? "Gravando..." : "Adicionar"}
            </Button>
          </div>
        </form>
      </Card>

      <Table>
        <THead>
          <Tr>
            <Th>Nome</Th>
            <Th className="w-24">País</Th>
            <Th className="w-32">Criticidade</Th>
            <Th className="w-56 text-right">Ações</Th>
          </Tr>
        </THead>
        <TBody>
          {loading && Array.from({ length: 5 }).map((_, i) => (
            <Tr key={i}>
              <Td colSpan={4}>
                <div className="h-5 w-full animate-pulse rounded bg-slate-800/60" />
              </Td>
            </Tr>
          ))}
          {!loading && rows.length === 0 && (
            <Tr>
              <Td colSpan={4}>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3 text-slate-300">
                    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" className="opacity-80">
                      <path d="M3 7h18M3 12h18M3 17h18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
                    </svg>
                    <span>Nenhum vendor cadastrado.</span>
                  </div>
                  <Button onClick={() => document.getElementById('name')?.focus()}>Adicionar primeiro vendor</Button>
                </div>
              </Td>
            </Tr>
          )}
          {!loading && rows.map((v) => (
            <Tr key={v.id} data-row={`vendor-${v.id}`}>
              <Td className="font-medium">{v.name}</Td>
              <Td>{v.country || "—"}</Td>
              <Td>
                <span className={`px-2 py-0.5 rounded-full text-xs border ${
                  v.criticality === "high"
                    ? "border-red-500/50 text-red-300"
                    : v.criticality === "medium"
                    ? "border-yellow-500/50 text-yellow-300"
                    : "border-green-500/50 text-green-300"
                }`}>{v.criticality || "low"}</span>
              </Td>
              <Td className="text-right space-x-2">
                <Button type="button" variant="ghost" onClick={() => startEdit(v)}>Editar</Button>
                <Button
                  type="button"
                  variant="destructive"
                  onClick={() => {
                    const rowEl = document.querySelector(`[data-row=\"vendor-${v.id}\"]`);
                    if (rowEl && rowEl.scrollIntoView) {
                      rowEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    }
                    setConfirmDlg({ open: true, id: v.id, name: v.name });
                  }}
                  disabled={rowAction === v.id}
                >
                  Excluir
                </Button>
              </Td>
            </Tr>
          ))}
        </TBody>
      </Table>

      {/* Dialog de edição */}
      {editingId !== null && (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
          <div className="absolute inset-0 bg-black/60" onClick={cancelEdit} />
          <div role="dialog" aria-modal="true" className="relative w-[92%] max-w-lg rounded-2xl border border-slate-700/60 bg-slate-900/90 p-6 shadow-2xl">
            <h3 className="text-lg font-semibold">Editar vendor</h3>
            <div className="mt-4 grid grid-cols-1 gap-3 sm:grid-cols-12">
              <div className="sm:col-span-6">
                <Label htmlFor="e-name">Nome</Label>
                <Input id="e-name" value={editForm.name} onChange={(e) => setEditForm({ ...editForm, name: e.target.value })} />
              </div>
              <div className="sm:col-span-3">
                <Label htmlFor="e-country">País</Label>
                <Input id="e-country" value={editForm.country || ""} onChange={(e) => setEditForm({ ...editForm, country: e.target.value })} />
              </div>
              <div className="sm:col-span-3">
                <Label htmlFor="e-criticality">Criticidade</Label>
                <Select id="e-criticality" value={editForm.criticality || "low"} onChange={(e) => setEditForm({ ...editForm, criticality: e.target.value })}>
                  <option value="low">low</option>
                  <option value="medium">medium</option>
                  <option value="high">high</option>
                </Select>
              </div>
            </div>
            <div className="mt-6 flex justify-end gap-2">
              <Button type="button" variant="secondary" onClick={cancelEdit}>Cancelar</Button>
              <Button type="button" onClick={() => saveEdit(editingId)} loading={rowAction === editingId}>Salvar</Button>
            </div>
          </div>
        </div>
      )}

      <ConfirmDialog
        open={confirmDlg.open}
        title="Confirmar exclusão"
        description={`Remover "${confirmDlg.name}"? Esta ação não poderá ser desfeita.`}
        destructive
        onCancel={() => setConfirmDlg({ open: false, id: null, name: "" })}
        onConfirm={() => removeConfirmed(confirmDlg.id)}
      />
    </div>
  );
}

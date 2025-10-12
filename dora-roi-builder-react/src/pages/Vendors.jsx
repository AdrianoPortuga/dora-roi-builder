import { useEffect, useMemo, useState } from 'react'
import api from '../api/client'

function Modal({ open, onClose, initial, onSave }){
  const [form, setForm] = useState(initial || { name:'', country:'PT', criticality:'low' })
  useEffect(()=>{ setForm(initial || { name:'', country:'PT', criticality:'low' }) }, [initial])
  if(!open) return null
  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50" onClick={(e)=>{ if(e.target===e.currentTarget) onClose() }}>
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 w-full max-w-lg">
        <h3 className="text-lg font-semibold mb-3">{initial ? 'Editar Vendor' : 'Novo Vendor'}</h3>
        <div className="grid grid-cols-2 gap-3">
          <div><label className="text-sm">Nome</label>
            <input className="w-full mt-1 px-3 py-2 rounded border border-slate-700 bg-slate-950" value={form.name} onChange={e=>setForm(v=>({...v, name:e.target.value}))}/>
          </div>
          <div><label className="text-sm">País (ISO2)</label>
            <input className="w-full mt-1 px-3 py-2 rounded border border-slate-700 bg-slate-950" maxLength={2} value={form.country} onChange={e=>setForm(v=>({...v, country:e.target.value.toUpperCase()}))}/>
          </div>
          <div><label className="text-sm">Criticidade</label>
            <select className="w-full mt-1 px-3 py-2 rounded border border-slate-700 bg-slate-950" value={form.criticality} onChange={e=>setForm(v=>({...v, criticality:e.target.value}))}>
              <option value="low">low</option><option value="medium">medium</option><option value="high">high</option>
            </select>
          </div>
        </div>
        <div className="flex justify-end gap-2 mt-4">
          <button className="px-3 py-2 rounded border border-slate-700" onClick={onClose}>Cancelar</button>
          <button className="px-3 py-2 rounded bg-blue-600 hover:bg-blue-500" onClick={()=>onSave(form)}>Salvar</button>
        </div>
      </div>
    </div>
  )
}

export default function Vendors(){
  const [list, setList] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [open, setOpen] = useState(false)
  const [editItem, setEdit] = useState(null)
  const [search, setSearch] = useState('')

  const fetchData = async () => {
    setLoading(true); setError('')
    try {
      const data = await api.getVendors()
      const arr = Array.isArray(data) ? data : (data.results || data.items || [])
      setList(arr)
    } catch (e) { setError(e?.response?.data?.detail || 'Falha ao carregar vendors') }
    finally { setLoading(false) }
  }
  useEffect(()=>{ fetchData() }, [])

  const filtered = useMemo(()=>{
    const q = search.trim().toLowerCase()
    if(!q) return list
    return list.filter(x => (x.name||'').toLowerCase().includes(q) || (x.country||'').toLowerCase().includes(q))
  }, [search, list])

  const onCreate = async (form) => { await api.createVendor(form); setOpen(false); await fetchData() }
  const onUpdate = async (form) => { await api.updateVendor(editItem.id, form); setEdit(null); await fetchData() }
  const onDelete = async (id) => { if (!confirm('Excluir vendor?')) return; await api.deleteVendor(id); await fetchData() }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-bold">Vendors</h2>
        <div className="flex items-center gap-2">
          <input placeholder="Pesquisar..." value={search} onChange={e=>setSearch(e.target.value)} className="px-3 py-2 rounded border border-slate-700 bg-slate-900"/>
          <button className="px-3 py-2 rounded bg-blue-600 hover:bg-blue-500" onClick={()=>setOpen(true)}>Novo Vendor</button>
        </div>
      </div>
      {error && <div className="text-red-400">{error}</div>}
      {loading ? <div>Carregando...</div> : (
        <div className="overflow-x-auto border border-slate-800 rounded-lg">
          <table className="min-w-full text-sm">
            <thead className="bg-slate-900 text-slate-300">
              <tr><th className="text-left p-3">ID</th><th className="text-left p-3">Nome</th><th className="text-left p-3">País</th><th className="text-left p-3">Criticidade</th><th className="text-right p-3">Ações</th></tr>
            </thead>
            <tbody>
              {filtered.map(v => (
                <tr key={v.id} className="border-t border-slate-800 hover:bg-slate-900/60">
                  <td className="p-3">{v.id}</td><td className="p-3">{v.name}</td><td className="p-3">{v.country}</td>
                  <td className="p-3"><span className="px-2 py-1 rounded border border-slate-700">{v.criticality}</span></td>
                  <td className="p-3 text-right space-x-2">
                    <button className="px-2 py-1 rounded border border-slate-700" onClick={()=>{ setEdit(v) }}>Editar</button>
                    <button className="px-2 py-1 rounded border border-slate-700" onClick={()=>onDelete(v.id)}>Excluir</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      <Modal open={open} onClose={()=>setOpen(false)} onSave={onCreate} />
      <Modal open={!!editItem} initial={editItem} onClose={()=>setEdit(null)} onSave={onUpdate} />
    </div>
  )
}

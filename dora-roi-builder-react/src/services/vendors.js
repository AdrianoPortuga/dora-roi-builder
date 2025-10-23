import { api } from "../api/client";

// GET /
export async function listVendors(query="") {
  const { data } = await api.get("/", { params: query ? { q: query } : undefined });
  return data;
}

// POST /
export async function createVendor(vendor) {
  const { data } = await api.post("/", vendor);
  return data;
}

// GET /{id}
export async function getVendor(id) {
  const { data } = await api.get(`/${id}`);
  return data;
}

// PUT /{id}
export async function updateVendor(id, vendor) {
  const { data } = await api.put(`/${id}`, vendor);
  return data;
}

// DELETE /{id}
export async function deleteVendor(id) {
  const { data } = await api.delete(`/${id}`);
  return data;
}

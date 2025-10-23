import axios from "axios";

// Base da API (defina em .env.local se quiser trocar)
const baseURL = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000/api/v1";

const instance = axios.create({
  baseURL,
  withCredentials: false,
});

// Seta/limpa Authorization global e persiste no localStorage
function setToken(token) {
  if (token) {
    instance.defaults.headers.common["Authorization"] = `Bearer ${token}`;
    try { localStorage.setItem("dora_token", token); } catch {}
  } else {
    delete instance.defaults.headers.common["Authorization"];
    try { localStorage.removeItem("dora_token"); } catch {}
  }
}

// Restaura token salvo ao carregar
try {
  const saved = localStorage.getItem("dora_token");
  if (saved) setToken(saved);
} catch {}

export const api = {
  // Auth
  login: async (email, password) => (await instance.post("/auth/login", { email, password })).data,
  me: async () => (await instance.get("/auth/me")).data,

  // Vendors (CRUD)
  listVendors: async () => (await instance.get("/vendors")).data,
  createVendor: async (payload) => (await instance.post("/vendors", payload)).data,
  updateVendor: async (id, payload) => (await instance.put(`/vendors/${id}`, payload)).data,
  deleteVendor: async (id) => (await instance.delete(`/vendors/${id}`)).data,
};

export { instance as http, setToken };
export default api; 

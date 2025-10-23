import axios from "axios";

export function resolveBaseURL(): string {
  const fromEnv = (import.meta as any).env?.VITE_API_BASE as string | undefined;
  const base = fromEnv && fromEnv.length > 0 ? fromEnv : "http://127.0.0.1:8000/api/v1";
  return base.replace(/\/+$/, "");
}

export const api = axios.create({
  baseURL: resolveBaseURL(),
  headers: {
    "Content-Type": "application/json",
    "Accept": "application/json",
  },
});

// Adiciona automaticamente o Authorization: Bearer <token>
api.interceptors.request.use((config) => {
  try {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers = config.headers ?? {};
      (config.headers as any).Authorization = `Bearer ${token}`;
    }
  } catch {}
  return config;
});

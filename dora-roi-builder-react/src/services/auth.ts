import { api } from "./api";

export async function api.login(email: string, password: string) {
  const { data } = await api.post("/auth/login", { email, password });
  if (data?.access_token) {
    localStorage.setItem("access_token", data.access_token);
  }
  return data;
}

export async function me() {
  const { data } = await api.get("/auth/me");
  return data;
}

export function logout() {
  localStorage.removeItem("access_token");
}

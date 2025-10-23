import { createContext, useContext, useEffect, useState } from "react";
import api, { setToken } from "../api/client";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Tenta restaurar sessão
  useEffect(() => {
    let mounted = true;
    api.me()
      .then((u) => mounted && setUser(u))
      .catch(() => mounted && setUser(null))
      .finally(() => mounted && setLoading(false));
    return () => { mounted = false; };
  }, []);

  const login = async (email, password) => {
    const res = await api.login(email, password); // { access_token: ... }
    setToken(res.access_token);
    const me = await api.me();
    setUser(me);
    return me;
  };

  const logout = () => {
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
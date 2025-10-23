import React, { createContext, useContext, useMemo, useState } from "react";

const ToastContext = createContext(null);

export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([]);

  const addToast = (toast) => {
    const id = Math.random().toString(36).slice(2);
    const item = { id, type: toast.type || "info", message: toast.message };
    setToasts((t) => [...t, item]);
    setTimeout(() => {
      setToasts((arr) => arr.filter((x) => x.id !== id));
    }, toast.duration || 2500);
  };

  const value = useMemo(() => ({ addToast }), []);

  return (
    <ToastContext.Provider value={value}>
      {children}
      <div className="pointer-events-none fixed top-4 right-4 z-50 space-y-2">
        {toasts.map((t) => (
          <div
            key={t.id}
            className={`pointer-events-auto rounded-xl border px-4 py-2 shadow-lg backdrop-blur text-sm ${
              t.type === "success"
                ? "bg-emerald-900/70 border-emerald-600/50 text-emerald-100"
                : t.type === "error"
                ? "bg-rose-900/70 border-rose-600/50 text-rose-100"
                : "bg-slate-800/70 border-slate-600/50 text-slate-100"
            }`}
          >
            {t.message}
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
}

export function useToast() {
  return useContext(ToastContext);
}


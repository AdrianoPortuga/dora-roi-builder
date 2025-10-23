import React from "react";
import Header from "../components/Header";
import { ToastProvider } from "../components/ToastProvider";

export default function PageShell({ children }) {
  return (
    <ToastProvider>
      <div className="min-h-screen bg-gradient-to-b from-[#0B1020] to-[#0D1B3D] text-slate-100">
        <Header />
        <main className="container mx-auto max-w-7xl px-4 py-8">{children}</main>
        <footer className="mt-10 border-t border-slate-700/40 py-6 text-center text-xs text-slate-400">
          DORA RoI Builder — MVP UI
        </footer>
      </div>
    </ToastProvider>
  );
}


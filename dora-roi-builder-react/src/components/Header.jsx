import React from "react";
import { Link, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import Button from "./ui/Button";

function NavLink({ to, children, disabled }) {
  const location = useLocation();
  const active = location.pathname.startsWith(to);
  const cls = disabled
    ? "opacity-60 cursor-not-allowed"
    : active
    ? "text-white bg-[#0e2b63]"
    : "hover:bg-[#0e2b63] hover:text-white";
  return (
    <Link to={disabled ? "#" : to} className={`px-3 py-2 rounded-xl ${cls}`} aria-disabled={disabled}>
      {children}
    </Link>
  );
}

export default function Header() {
  const { user, logout } = useAuth();
  return (
    <header className="sticky top-0 z-40 border-b border-[#1e3a8a]/40 bg-[#0a1b3e]/80 backdrop-blur">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3">
        <div className="flex items-center gap-3">
          <div className="h-6 w-6 rounded bg-blue-600" />
          <div className="font-semibold">DORA RoI Builder</div>
          <span className="text-xs px-2 py-1 rounded-full border border-blue-500/40 text-blue-300">MVP UI</span>
        </div>
        <nav className="hidden gap-2 md:flex text-slate-200">
          <NavLink to="/vendors">Vendors</NavLink>
          <span className="px-3 py-2 rounded-xl opacity-60">Riscos</span>
          <span className="px-3 py-2 rounded-xl opacity-60">Evidências</span>
          <span className="px-3 py-2 rounded-xl opacity-60">Relatórios</span>
        </nav>
        <div className="flex items-center gap-3">
          <span className="text-sm text-slate-200 hidden sm:block">{user?.email}</span>
          <Button variant="secondary" onClick={logout}>Sair</Button>
        </div>
      </div>
    </header>
  );
}


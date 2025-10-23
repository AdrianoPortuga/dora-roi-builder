import React from "react";

export default function Card({ className = "", children }) {
  return (
    <div className={`rounded-2xl border border-slate-700/50 bg-slate-900/60 backdrop-blur p-6 shadow-lg ${className}`}>
      {children}
    </div>
  );
}


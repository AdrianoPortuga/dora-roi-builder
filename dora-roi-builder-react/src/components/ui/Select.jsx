import React from "react";

export default function Select({ className = "", children, ...props }) {
  return (
    <select
      className={`w-full rounded-xl border border-slate-700 bg-slate-800/60 px-3 py-2 text-slate-100 focus:outline-none focus:ring-2 focus:ring-blue-400 ${className}`}
      {...props}
    >
      {children}
    </select>
  );
}


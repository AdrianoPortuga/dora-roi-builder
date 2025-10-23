import React from "react";

export function Label({ htmlFor, children, className = "" }) {
  return (
    <label htmlFor={htmlFor} className={`block text-sm font-medium text-slate-300 mb-1 ${className}`}>
      {children}
    </label>
  );
}

export default function Input({ className = "", ...props }) {
  return (
    <input
      className={`w-full rounded-xl border border-slate-700 bg-slate-800/60 px-3 py-2 text-slate-100 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-400 ${className}`}
      {...props}
    />
  );
}


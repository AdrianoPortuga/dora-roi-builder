import React from "react";

export function Table({ children, className = "" }) {
  return (
    <div className={`overflow-x-auto rounded-2xl border border-slate-700/50 bg-slate-900/50 ${className}`}>
      <table className="w-full text-sm">{children}</table>
    </div>
  );
}

export function THead({ children }) {
  return <thead className="bg-slate-800/70 text-slate-300">{children}</thead>;
}

export function Tr({ children, className = "", ...props }) {
  return (
    <tr className={`hover:bg-slate-800/40 ${className}`} {...props}>
      {children}
    </tr>
  );
}

export function Th({ children, className = "" }) {
  return <th className={`px-4 py-3 text-left text-sm font-semibold ${className}`}>{children}</th>;
}

export function TBody({ children }) {
  return <tbody className="divide-y divide-slate-800/60">{children}</tbody>;
}

export function Td({ children, className = "", ...props }) {
  return (
    <td className={`px-4 py-3 text-sm text-slate-200 ${className}`} {...props}>
      {children}
    </td>
  );
}

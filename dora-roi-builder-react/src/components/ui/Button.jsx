import React from "react";

const base =
  "inline-flex items-center justify-center gap-2 rounded-xl font-medium focus:outline-none focus:ring-2 focus:ring-blue-400 disabled:opacity-60 disabled:cursor-not-allowed transition-colors";

const variants = {
  primary:
    "bg-blue-600 text-white hover:bg-blue-700 px-4 py-2",
  secondary:
    "bg-slate-700 text-slate-100 hover:bg-slate-600 px-3 py-2",
  ghost:
    "px-3 py-2 hover:bg-slate-800/60 text-slate-100",
  destructive:
    "bg-rose-600 text-white hover:bg-rose-700 px-3 py-2 focus:ring-rose-400",
};

const sizes = {
  sm: "text-sm",
  md: "text-sm",
};

export default function Button({
  variant = "primary",
  size = "md",
  loading = false,
  className = "",
  children,
  ...props
}) {
  return (
    <button
      aria-busy={loading}
      className={`${base} ${variants[variant]} ${sizes[size]} ${className}`}
      {...props}
    >
      {loading && (
        <svg
          className="h-4 w-4 animate-spin"
          viewBox="0 0 24 24"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z" />
        </svg>
      )}
      {children}
    </button>
  );
}


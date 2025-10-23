import React, { useEffect } from "react";
import Button from "./ui/Button";

export default function ConfirmDialog({
  open,
  title = "Confirmar",
  description = "Tem certeza?",
  confirmText = "Confirmar",
  cancelText = "Cancelar",
  destructive = false,
  onConfirm,
  onCancel,
}) {
  useEffect(() => {
    function onKey(e) {
      if (e.key === "Escape" && open) onCancel?.();
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open, onCancel]);

  if (!open) return null;
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div className="absolute inset-0 bg-black/60" onClick={onCancel} />
      <div
        role="dialog"
        aria-modal="true"
        className="relative w-[92%] max-w-md rounded-2xl border border-slate-700/60 bg-slate-900/90 p-6 shadow-2xl"
      >
        <h3 className="text-lg font-semibold text-slate-100">{title}</h3>
        <p className="mt-1 text-sm text-slate-300">{description}</p>
        <div className="mt-5 flex justify-end gap-2">
          <Button variant="secondary" onClick={onCancel}>{cancelText}</Button>
          <Button autoFocus variant={destructive ? "destructive" : "primary"} onClick={onConfirm}>
            {confirmText}
          </Button>
        </div>
      </div>
    </div>
  );
}

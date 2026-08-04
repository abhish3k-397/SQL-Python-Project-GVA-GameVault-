import React from 'react';
import { CheckCircle2, AlertCircle, Info, X } from 'lucide-react';

export default function Toast({ toast, onClose }) {
  if (!toast) return null;

  const icons = {
    success: <CheckCircle2 size={16} color="#ffffff" />,
    error: <AlertCircle size={16} color="#ffffff" />,
    info: <Info size={16} color="#a1a1aa" />
  };

  return (
    <div style={{
      position: 'fixed',
      bottom: '24px',
      right: '24px',
      zIndex: 2000,
      background: '#09090b',
      border: '1px solid #27272a',
      boxShadow: '0 15px 40px rgba(0,0,0,0.8)',
      borderRadius: '8px',
      padding: '12px 18px',
      display: 'flex',
      alignItems: 'center',
      gap: '10px',
      color: '#fff',
      animation: 'slideUp 0.25s ease-out',
      maxWidth: '380px'
    }}>
      {icons[toast.type] || icons.info}
      <span style={{ fontSize: '0.85rem', fontWeight: 500, flex: 1 }}>{toast.message}</span>
      <button 
        onClick={onClose}
        style={{ background: 'none', border: 'none', color: '#71717a', cursor: 'pointer', padding: 2 }}
      >
        <X size={14} />
      </button>
    </div>
  );
}

import React, { useState } from 'react';
import { X, Wallet, PlusCircle } from 'lucide-react';

export default function WalletModal({ isOpen, onClose, user, onDeposit }) {
  const [amount, setAmount] = useState('500');
  const [loading, setLoading] = useState(false);

  if (!isOpen || !user) return null;

  const handleDepositSubmit = async (e) => {
    e.preventDefault();
    const val = parseFloat(amount);
    if (!val || val <= 0) return;
    setLoading(true);
    await onDeposit(val);
    setLoading(false);
    onClose();
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-card" onClick={(e) => e.stopPropagation()} style={{ maxWidth: '420px', padding: '24px', background: '#0f0f12', border: '1px solid #27272a' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '18px' }}>
          <h3 style={{ fontSize: '1.2rem', color: '#fff', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Wallet size={18} /> Wallet Balance
          </h3>
          <button onClick={onClose} className="btn btn-ghost btn-icon"><X size={16} /></button>
        </div>

        {/* Current Balance Display */}
        <div style={{
          padding: '16px',
          background: '#141417',
          border: '1px solid #27272a',
          borderRadius: '10px',
          textAlign: 'center',
          marginBottom: '20px'
        }}>
          <span style={{ fontSize: '0.8rem', color: '#71717a' }}>Available Funds</span>
          <h2 style={{ fontSize: '2rem', fontWeight: 700, color: '#ffffff', marginTop: '2px' }}>
            ₹{user.wallet_balance.toFixed(2)}
          </h2>
        </div>

        <form onSubmit={handleDepositSubmit}>
          <span style={{ fontSize: '0.8rem', color: '#71717a', display: 'block', marginBottom: '8px' }}>
            Select Amount
          </span>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '8px', marginBottom: '14px' }}>
            {['200', '500', '1000', '2500'].map((val) => (
              <button
                key={val}
                type="button"
                onClick={() => setAmount(val)}
                className={`btn ${amount === val ? 'btn-primary' : 'btn-secondary'}`}
                style={{ padding: '8px 0', fontSize: '0.8rem' }}
              >
                ₹{val}
              </button>
            ))}
          </div>

          <div style={{ marginBottom: '16px' }}>
            <input
              type="number"
              min="1"
              step="1"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              placeholder="Or enter custom amount"
              style={{
                width: '100%',
                padding: '10px 14px',
                borderRadius: '6px',
                background: '#09090b',
                border: '1px solid #27272a',
                color: '#fff',
                outline: 'none',
                fontSize: '0.9rem'
              }}
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="btn btn-primary"
            style={{ width: '100%', padding: '10px', fontSize: '0.9rem' }}
          >
            <PlusCircle size={16} /> {loading ? 'Processing...' : 'Deposit Funds'}
          </button>
        </form>
      </div>
    </div>
  );
}

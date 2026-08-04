import React, { useState } from 'react';
import { X, Trash2, ShoppingBag, Wallet, CreditCard } from 'lucide-react';

export default function CartDrawer({
  isOpen,
  onClose,
  cartItems,
  user,
  onRemoveFromCart,
  onCheckout,
  onOpenAuth
}) {
  const [paymentMethod, setPaymentMethod] = useState('Wallet');
  const [checkingOut, setCheckingOut] = useState(false);

  if (!isOpen) return null;

  const totalAmount = cartItems.reduce((acc, item) => acc + item.final_price, 0);
  const userBalance = user ? user.wallet_balance : 0;
  const hasEnoughFunds = paymentMethod === 'Wallet' ? userBalance >= totalAmount : true;

  const handleCheckoutClick = async () => {
    if (!user) {
      onOpenAuth();
      return;
    }
    setCheckingOut(true);
    await onCheckout(cartItems.map(i => i.game_id), paymentMethod);
    setCheckingOut(false);
  };

  return (
    <div className="modal-overlay" onClick={onClose} style={{ justifyContent: 'flex-end', padding: 0 }}>
      <div style={{
        width: '100%',
        maxWidth: '380px',
        height: '100vh',
        background: '#09090b',
        borderLeft: '1px solid #1f1f23',
        display: 'flex',
        flexDirection: 'column',
        boxShadow: '-10px 0 40px rgba(0, 0, 0, 0.9)',
        animation: 'slideUp 0.2s ease-out'
      }} onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div style={{
          padding: '14px 20px',
          borderBottom: '1px solid #1f1f23',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between'
        }}>
          <h3 style={{ fontSize: '1rem', color: '#fff', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <ShoppingBag size={16} /> Cart ({cartItems.length})
          </h3>
          <button onClick={onClose} className="btn btn-ghost btn-icon">
            <X size={16} />
          </button>
        </div>

        {/* Cart Items List */}
        <div style={{ flex: 1, overflowY: 'auto', padding: '16px' }}>
          {cartItems.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '40px 20px', color: '#52525b' }}>
              <ShoppingBag size={36} style={{ opacity: 0.3, marginBottom: '10px' }} />
              <p style={{ fontSize: '12px' }}>Your cart is empty.</p>
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              {cartItems.map((item) => (
                <div key={item.game_id} style={{
                  display: 'flex',
                  gap: '10px',
                  padding: '8px',
                  background: '#121215',
                  borderRadius: '6px',
                  border: '1px solid #1f1f23'
                }}>
                  <img
                    src={item.cover_image}
                    alt={item.title}
                    style={{ width: '48px', height: '48px', borderRadius: '4px', objectFit: 'cover' }}
                  />
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <h4 style={{ fontSize: '0.85rem', color: '#fff', marginBottom: '2px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{item.title}</h4>
                    <span style={{ fontSize: '0.8rem', fontWeight: 700, color: '#ffffff' }}>
                      ₹{item.final_price.toFixed(2)}
                    </span>
                  </div>
                  <button
                    onClick={() => onRemoveFromCart(item.game_id)}
                    className="btn btn-ghost btn-icon"
                    style={{ color: '#71717a', alignSelf: 'center' }}
                  >
                    <Trash2 size={14} />
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Footer Summary & Checkout */}
        {cartItems.length > 0 && (
          <div style={{
            padding: '16px 20px',
            borderTop: '1px solid #1f1f23',
            background: '#0d0d10'
          }}>
            {/* Payment Method Selector */}
            <div style={{ marginBottom: '12px' }}>
              <span style={{ fontSize: '10px', color: '#52525b', display: 'block', marginBottom: '4px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Payment Method</span>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '6px' }}>
                <button
                  onClick={() => setPaymentMethod('Wallet')}
                  className={`btn ${paymentMethod === 'Wallet' ? 'btn-primary' : 'btn-secondary'}`}
                  style={{ fontSize: '11px', padding: '6px' }}
                >
                  <Wallet size={12} /> Wallet
                </button>
                <button
                  onClick={() => setPaymentMethod('Credit Card')}
                  className={`btn ${paymentMethod === 'Credit Card' ? 'btn-primary' : 'btn-secondary'}`}
                  style={{ fontSize: '11px', padding: '6px' }}
                >
                  <CreditCard size={12} /> Card
                </button>
              </div>
            </div>

            {/* Total Amount */}
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '12px' }}>
              <span style={{ color: '#a1a1aa', fontSize: '12px' }}>Total Amount</span>
              <span style={{ fontSize: '1.1rem', fontWeight: 700, color: '#fff' }}>₹{totalAmount.toFixed(2)}</span>
            </div>

            {paymentMethod === 'Wallet' && user && !hasEnoughFunds && (
              <p style={{ color: '#ffffff', fontSize: '11px', marginBottom: '8px', textAlign: 'center', background: '#18181b', padding: '4px 6px', borderRadius: '4px', border: '1px solid #27272a' }}>
                Insufficient balance (₹{userBalance.toFixed(2)}). Use Card or Deposit.
              </p>
            )}

            <button
              onClick={handleCheckoutClick}
              disabled={checkingOut || (paymentMethod === 'Wallet' && user && !hasEnoughFunds)}
              className="btn btn-primary"
              style={{ width: '100%', padding: '10px', fontSize: '12px' }}
            >
              {user ? (checkingOut ? 'Processing...' : 'Complete Checkout') : 'Sign In to Buy'}
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

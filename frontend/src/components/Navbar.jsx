import React from 'react';
import { Search, ShoppingBag, Wallet, User, Plus } from 'lucide-react';

export default function Navbar({
  user,
  cartCount,
  searchQuery,
  setSearchQuery,
  onOpenCart,
  onOpenWallet,
  onNavigateLogin
}) {
  return (
    <header className="top-bar">
      {/* Global Search Bar */}
      <div style={{ flex: 1, maxWidth: '420px', position: 'relative' }}>
        <Search size={14} style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)', color: '#52525b' }} />
        <input
          type="text"
          placeholder="Search games, developers, genres..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          style={{
            width: '100%',
            padding: '6px 12px 6px 34px',
            borderRadius: '5px',
            background: '#121215',
            border: '1px solid #1f1f23',
            color: '#ffffff',
            fontSize: '12px',
            outline: 'none',
            transition: 'border-color 0.15s ease'
          }}
        />
      </div>

      {/* Top Right Quick Actions */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
        <button
          onClick={onOpenCart}
          className="btn btn-secondary"
          style={{ position: 'relative', padding: '6px 10px' }}
        >
          <ShoppingBag size={14} />
          <span>Cart</span>
          {cartCount > 0 && (
            <span style={{
              background: '#ffffff',
              color: '#000000',
              borderRadius: '999px',
              padding: '0 5px',
              fontSize: '10px',
              fontWeight: 700,
              marginLeft: '2px'
            }}>
              {cartCount}
            </span>
          )}
        </button>

        {user ? (
          <div 
            onClick={onOpenWallet}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              background: '#141417',
              border: '1px solid #1f1f23',
              borderRadius: '5px',
              padding: '5px 10px',
              cursor: 'pointer'
            }}
          >
            <Wallet size={13} color="#fafafa" />
            <span style={{ fontSize: '11px', fontWeight: 600, color: '#ffffff' }}>
              ₹{user.wallet_balance.toFixed(2)}
            </span>
            <Plus size={11} color="#a1a1aa" />
          </div>
        ) : (
          <button onClick={onNavigateLogin} className="btn btn-primary" style={{ padding: '5px 12px' }}>
            <User size={12} /> Sign In
          </button>
        )}
      </div>
    </header>
  );
}

import React from 'react';
import { Gamepad2, ShoppingBag, Heart, Library, ShieldCheck, Wallet, User, LogOut, Lock } from 'lucide-react';

export default function Sidebar({
  activeTab,
  setActiveTab,
  selectedGenre,
  setSelectedGenre,
  genres,
  user,
  cartCount,
  wishlistCount,
  onOpenCart,
  onOpenWallet,
  onLogout
}) {
  return (
    <aside className="sidebar">
      {/* Sidebar Header */}
      <div className="sidebar-header">
        <div style={{
          width: '26px',
          height: '26px',
          borderRadius: '4px',
          background: '#ffffff',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center'
        }}>
          <Gamepad2 size={16} color="#000000" />
        </div>
        <span style={{
          fontSize: '1.05rem',
          fontWeight: '700',
          fontFamily: 'var(--font-heading)',
          color: '#ffffff',
          letterSpacing: '-0.02em'
        }}>
          GAMEVAULT
        </span>
      </div>

      {/* Navigation Groups */}
      <div className="sidebar-content">
        {/* STORE CATALOG */}
        <div className="sidebar-section-title">0 · Store Catalog</div>
        
        <div
          className={`sidebar-item ${activeTab === 'store' && selectedGenre === '' ? 'active' : ''}`}
          onClick={() => { setActiveTab('store'); setSelectedGenre(''); }}
        >
          <span>All Titles</span>
        </div>

        {/* GENRES */}
        <div className="sidebar-section-title">I · Browse Genres</div>
        {genres && genres.slice(0, 6).map((g) => (
          <div
            key={g.genre_id}
            className={`sidebar-item ${activeTab === 'store' && selectedGenre === g.name ? 'active' : ''}`}
            onClick={() => { setActiveTab('store'); setSelectedGenre(g.name); }}
          >
            <span>{g.name}</span>
          </div>
        ))}

        {/* MY COLLECTION */}
        <div className="sidebar-section-title">II · My Vault</div>
        {user ? (
          <>
            <div
              className={`sidebar-item ${activeTab === 'library' ? 'active' : ''}`}
              onClick={() => setActiveTab('library')}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Library size={13} />
                <span>My Library</span>
              </div>
            </div>

            <div
              className={`sidebar-item ${activeTab === 'wishlist' ? 'active' : ''}`}
              onClick={() => setActiveTab('wishlist')}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Heart size={13} />
                <span>Wishlist</span>
              </div>
              {wishlistCount > 0 && (
                <span style={{ fontSize: '10px', background: '#27272a', color: '#fff', padding: '1px 6px', borderRadius: '3px' }}>
                  {wishlistCount}
                </span>
              )}
            </div>
          </>
        ) : (
          <div className="sidebar-item" onClick={() => setActiveTab('login')}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: '#71717a' }}>
              <Lock size={13} />
              <span>Sign in for Library</span>
            </div>
          </div>
        )}

        <div className="sidebar-item" onClick={onOpenCart}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <ShoppingBag size={13} />
            <span>Shopping Cart</span>
          </div>
          {cartCount > 0 && (
            <span style={{ fontSize: '10px', background: '#ffffff', color: '#000000', padding: '1px 6px', borderRadius: '3px', fontWeight: 700 }}>
              {cartCount}
            </span>
          )}
        </div>

        {/* MANAGEMENT */}
        {user && user.role === 'admin' && (
          <>
            <div className="sidebar-section-title">III · Management</div>
            <div
              className={`sidebar-item ${activeTab === 'admin' ? 'active' : ''}`}
              onClick={() => setActiveTab('admin')}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <ShieldCheck size={13} />
                <span>Admin Dashboard</span>
              </div>
            </div>
          </>
        )}
      </div>

      {/* Sidebar Footer */}
      <div className="sidebar-footer">
        {user ? (
          <div>
            <div 
              onClick={onOpenWallet}
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                padding: '8px 10px',
                background: '#141417',
                border: '1px solid #1f1f23',
                borderRadius: '5px',
                cursor: 'pointer',
                marginBottom: '8px'
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                <Wallet size={13} color="#fafafa" />
                <span style={{ fontSize: '11px', color: '#a1a1aa' }}>Wallet</span>
              </div>
              <span style={{ fontSize: '12px', fontWeight: 600, color: '#ffffff' }}>
                ₹{user.wallet_balance.toFixed(2)}
              </span>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '4px 6px' }}>
              <span style={{ fontSize: '11px', color: '#71717a', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', maxWidth: '140px' }}>
                {user.username} {user.role === 'admin' ? '(Admin)' : ''}
              </span>
              <button 
                onClick={onLogout}
                className="btn btn-ghost btn-icon"
                title="Sign out"
                style={{ padding: '4px', color: '#71717a' }}
              >
                <LogOut size={13} />
              </button>
            </div>
          </div>
        ) : (
          <button
            onClick={() => setActiveTab('login')}
            className={`btn ${activeTab === 'login' ? 'btn-primary' : 'btn-secondary'}`}
            style={{ width: '100%', padding: '8px' }}
          >
            <User size={13} /> Sign In Page
          </button>
        )}
      </div>
    </aside>
  );
}

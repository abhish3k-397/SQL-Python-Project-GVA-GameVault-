import React from 'react';
import { Heart, ShoppingBag, Trash2 } from 'lucide-react';

export default function WishlistView({ wishlist, onAddToCart, onRemoveFromWishlist, onSelectGame }) {
  if (!wishlist || wishlist.length === 0) {
    return (
      <div style={{ textAlign: 'center', padding: '80px 20px', color: '#71717a' }}>
        <Heart size={56} style={{ opacity: 0.3, marginBottom: '16px' }} />
        <h2 style={{ color: '#fff', marginBottom: '8px' }}>Your Wishlist is Empty</h2>
        <p>Save games you want to purchase later.</p>
      </div>
    );
  }

  return (
    <div>
      <div style={{ marginBottom: '24px' }}>
        <h2 style={{ fontSize: '1.6rem', color: '#fff', marginBottom: '4px' }}>Wishlist</h2>
        <p style={{ color: '#a1a1aa', fontSize: '0.9rem' }}>{wishlist.length} saved titles</p>
      </div>

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(260px, 1fr))',
        gap: '20px'
      }}>
        {wishlist.map((game) => (
          <div key={game.game_id} className="glass-panel" style={{ overflow: 'hidden', display: 'flex', flexDirection: 'column', background: '#121215', border: '1px solid #27272a' }}>
            <div 
              onClick={() => onSelectGame(game)}
              style={{ position: 'relative', height: '160px', cursor: 'pointer' }}
            >
              <img
                src={game.cover_image}
                alt={game.title}
                style={{ width: '100%', height: '100%', objectFit: 'cover', filter: 'grayscale(30%)' }}
              />
              {game.discount_percent > 0 && (
                <div style={{ position: 'absolute', top: 10, left: 10 }}>
                  <span className="badge badge-discount">-{game.discount_percent}%</span>
                </div>
              )}
            </div>

            <div style={{ padding: '16px', flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
              <div>
                <h3 onClick={() => onSelectGame(game)} style={{ fontSize: '1rem', color: '#fff', marginBottom: '4px', cursor: 'pointer' }}>
                  {game.title}
                </h3>
                <span style={{ fontSize: '1.05rem', fontWeight: 700, color: '#ffffff' }}>
                  ₹{game.final_price.toFixed(2)}
                </span>
              </div>

              <div style={{ display: 'flex', gap: '8px', marginTop: '14px' }}>
                <button
                  onClick={() => onAddToCart(game)}
                  className="btn btn-primary"
                  style={{ flex: 1, padding: '6px', fontSize: '0.8rem' }}
                >
                  <ShoppingBag size={13} /> Add to Cart
                </button>
                <button
                  onClick={() => onRemoveFromWishlist(game.game_id)}
                  className="btn btn-secondary btn-icon"
                  style={{ color: '#71717a' }}
                  title="Remove from Wishlist"
                >
                  <Trash2 size={15} />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

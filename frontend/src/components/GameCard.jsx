import React from 'react';
import { Star, Heart, ShoppingBag } from 'lucide-react';

export default function GameCard({
  game,
  isWishlisted,
  isOwned,
  onSelectGame,
  onAddToCart,
  onToggleWishlist
}) {
  return (
    <div className="glass-panel" style={{
      display: 'flex',
      flexDirection: 'column',
      overflow: 'hidden',
      position: 'relative',
      height: '100%',
      background: '#121215',
      border: '1px solid #1f1f23'
    }}>
      {/* Cover Image */}
      <div 
        onClick={() => onSelectGame(game)}
        style={{
          position: 'relative',
          height: '145px',
          cursor: 'pointer',
          overflow: 'hidden',
          background: '#09090b'
        }}
      >
        <img
          src={game.cover_image}
          alt={game.title}
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            filter: 'grayscale(20%) contrast(1.1)',
            transition: 'transform 0.2s ease, filter 0.2s ease'
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.transform = 'scale(1.03)';
            e.currentTarget.style.filter = 'grayscale(0%) contrast(1)';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.transform = 'scale(1)';
            e.currentTarget.style.filter = 'grayscale(20%) contrast(1.1)';
          }}
        />

        {/* Wishlist Button */}
        <button
          onClick={(e) => {
            e.stopPropagation();
            onToggleWishlist(game);
          }}
          style={{
            position: 'absolute',
            top: '8px',
            right: '8px',
            background: isWishlisted ? '#ffffff' : 'rgba(9, 9, 11, 0.85)',
            border: '1px solid #27272a',
            borderRadius: '50%',
            width: '28px',
            height: '28px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            cursor: 'pointer',
            color: isWishlisted ? '#000000' : '#ffffff',
            transition: 'all 0.15s ease'
          }}
        >
          <Heart size={13} fill={isWishlisted ? '#000000' : 'none'} />
        </button>

        {/* Discount Badge */}
        {game.discount_percent > 0 && (
          <div style={{
            position: 'absolute',
            bottom: '8px',
            left: '8px'
          }}>
            <span className="badge badge-discount" style={{ fontSize: '10px', padding: '1px 5px' }}>
              -{game.discount_percent}%
            </span>
          </div>
        )}
      </div>

      {/* Info Container */}
      <div style={{
        padding: '12px',
        display: 'flex',
        flexDirection: 'column',
        flex: 1,
        justifyContent: 'space-between'
      }}>
        <div>
          {/* Developer & Rating */}
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '4px' }}>
            <span style={{ fontSize: '10px', color: '#52525b', fontWeight: 600, textTransform: 'uppercase' }}>
              {game.developer}
            </span>
            <div style={{ display: 'flex', alignItems: 'center', gap: '3px' }}>
              <Star size={11} style={{ fill: '#ffffff', color: '#ffffff' }} />
              <span style={{ fontSize: '11px', fontWeight: 600, color: '#ffffff' }}>
                {game.rating}
              </span>
            </div>
          </div>

          {/* Title */}
          <h3 
            onClick={() => onSelectGame(game)}
            style={{
              fontSize: '0.9rem',
              color: '#ffffff',
              marginBottom: '4px',
              cursor: 'pointer',
              whiteSpace: 'nowrap',
              overflow: 'hidden',
              textOverflow: 'ellipsis'
            }}
          >
            {game.title}
          </h3>
        </div>

        {/* Price & Action */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          marginTop: '10px',
          paddingTop: '8px',
          borderTop: '1px solid #1f1f23'
        }}>
          <div>
            {game.discount_percent > 0 ? (
              <div>
                <span style={{ fontSize: '10px', color: '#52525b', textDecoration: 'line-through', marginRight: '4px' }}>
                  ₹{game.original_price.toFixed(2)}
                </span>
                <span style={{ fontSize: '0.95rem', fontWeight: 700, color: '#ffffff' }}>
                  ₹{game.final_price.toFixed(2)}
                </span>
              </div>
            ) : (
              <span style={{ fontSize: '0.95rem', fontWeight: 700, color: '#ffffff' }}>
                ₹{game.final_price.toFixed(2)}
              </span>
            )}
          </div>

          {isOwned ? (
            <span style={{ fontSize: '10px', fontWeight: 600, color: '#fafafa', background: '#18181b', border: '1px solid #27272a', padding: '3px 6px', borderRadius: '3px' }}>
              Owned
            </span>
          ) : (
            <button
              onClick={() => onAddToCart(game)}
              className="btn btn-primary"
              style={{ padding: '4px 10px', fontSize: '11px' }}
            >
              <ShoppingBag size={11} /> Add
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

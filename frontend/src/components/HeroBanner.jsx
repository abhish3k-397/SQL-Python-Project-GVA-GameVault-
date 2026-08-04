import React from 'react';
import { Play, Star } from 'lucide-react';

export default function HeroBanner({ game, onSelectGame, onAddToCart }) {
  if (!game) return null;

  return (
    <div style={{
      position: 'relative',
      borderRadius: 'var(--radius-md)',
      overflow: 'hidden',
      marginBottom: '24px',
      height: '260px',
      border: '1px solid #1f1f23',
      background: '#0d0d10'
    }}>
      {/* Background Image with Monochromatic Overlay */}
      <img
        src={game.cover_image}
        alt={game.title}
        style={{
          width: '100%',
          height: '100%',
          objectFit: 'cover',
          filter: 'grayscale(60%) brightness(0.35) contrast(1.2)'
        }}
      />

      {/* Dark Fade Overlay */}
      <div style={{
        position: 'absolute',
        inset: 0,
        background: 'linear-gradient(90deg, #09090b 0%, rgba(9,9,11,0.65) 60%, transparent 100%)'
      }} />

      {/* Content */}
      <div style={{
        position: 'absolute',
        inset: 0,
        padding: '24px 32px',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        maxWidth: '540px'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '8px' }}>
          <span className="badge badge-discount" style={{ fontSize: '10px', padding: '2px 6px' }}>
            Featured Title
          </span>
          {game.discount_percent > 0 && (
            <span className="badge badge-rating" style={{ fontSize: '10px', padding: '2px 6px' }}>
              -{game.discount_percent}% OFF
            </span>
          )}
          <span className="badge badge-genre" style={{ fontSize: '10px', padding: '2px 6px' }}>
            <Star size={11} style={{ fill: '#ffffff', color: '#ffffff', marginRight: 3 }} />
            {game.rating}
          </span>
        </div>

        <h1 style={{
          fontSize: '1.8rem',
          fontWeight: 700,
          color: '#ffffff',
          marginBottom: '6px',
          lineHeight: 1.15
        }}>
          {game.title}
        </h1>

        <p style={{
          color: '#a1a1aa',
          fontSize: '12px',
          lineHeight: 1.45,
          marginBottom: '16px',
          display: '-webkit-box',
          WebkitLineClamp: 2,
          WebkitBoxOrient: 'vertical',
          overflow: 'hidden'
        }}>
          {game.description}
        </p>

        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <button onClick={() => onAddToCart(game)} className="btn btn-primary" style={{ padding: '6px 14px', fontSize: '12px' }}>
            Buy Now — ₹{game.final_price.toFixed(2)}
          </button>
          
          <button onClick={() => onSelectGame(game)} className="btn btn-secondary" style={{ padding: '6px 12px', fontSize: '12px' }}>
            <Play size={12} /> Details
          </button>
        </div>
      </div>
    </div>
  );
}

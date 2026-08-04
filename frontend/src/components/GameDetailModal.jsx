import React, { useState } from 'react';
import { X, Star, ShoppingBag, Heart, Check, Building, Calendar, Shield, MessageSquare, Send } from 'lucide-react';

export default function GameDetailModal({
  game,
  user,
  isOwned,
  isWishlisted,
  onClose,
  onAddToCart,
  onToggleWishlist,
  onSubmitReview
}) {
  const [rating, setRating] = useState(5);
  const [comment, setComment] = useState('');
  const [submitting, setSubmitting] = useState(false);

  if (!game) return null;

  const handleReviewSubmit = async (e) => {
    e.preventDefault();
    if (!comment.trim()) return;
    setSubmitting(true);
    await onSubmitReview(game.game_id, rating, comment);
    setComment('');
    setSubmitting(false);
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-card" onClick={(e) => e.stopPropagation()} style={{ maxWidth: '700px', background: '#0f0f12', border: '1px solid #27272a' }}>
        {/* Cover Header */}
        <div style={{ position: 'relative', height: '240px' }}>
          <img
            src={game.cover_image}
            alt={game.title}
            style={{ width: '100%', height: '100%', objectFit: 'cover', filter: 'brightness(0.5) contrast(1.1)' }}
          />
          <div style={{
            position: 'absolute',
            inset: 0,
            background: 'linear-gradient(0deg, #0f0f12 0%, transparent 100%)'
          }} />

          <button
            onClick={onClose}
            style={{
              position: 'absolute',
              top: '16px',
              right: '16px',
              background: '#18181b',
              border: '1px solid #27272a',
              borderRadius: '50%',
              width: '32px',
              height: '32px',
              color: '#fff',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}
          >
            <X size={16} />
          </button>

          <div style={{
            position: 'absolute',
            bottom: '20px',
            left: '24px',
            right: '24px'
          }}>
            <h2 style={{ fontSize: '1.8rem', color: '#fff', marginBottom: '6px' }}>{game.title}</h2>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
              <span className="badge badge-rating">
                <Star size={12} style={{ fill: '#ffffff', color: '#ffffff', marginRight: 4 }} />
                {game.rating} / 5.0 ({game.review_count || 0} reviews)
              </span>
              <span className="badge badge-genre">{game.age_rating || 'M'}</span>
              {game.genres && game.genres.map((g, idx) => (
                <span key={idx} className="badge badge-genre">{g}</span>
              ))}
            </div>
          </div>
        </div>

        {/* Content Body */}
        <div style={{ padding: '24px' }}>
          {/* Metadata Bar */}
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(3, 1fr)',
            gap: '12px',
            marginBottom: '20px',
            background: '#141417',
            padding: '14px',
            borderRadius: '8px',
            border: '1px solid #27272a'
          }}>
            <div>
              <span style={{ fontSize: '0.75rem', color: '#71717a', display: 'flex', alignItems: 'center', gap: 4 }}>
                <Building size={13} /> Developer
              </span>
              <p style={{ fontWeight: 600, fontSize: '0.85rem', color: '#fff', marginTop: 2 }}>{game.developer}</p>
            </div>
            <div>
              <span style={{ fontSize: '0.75rem', color: '#71717a', display: 'flex', alignItems: 'center', gap: 4 }}>
                <Shield size={13} /> Publisher
              </span>
              <p style={{ fontWeight: 600, fontSize: '0.85rem', color: '#fff', marginTop: 2 }}>{game.publisher}</p>
            </div>
            <div>
              <span style={{ fontSize: '0.75rem', color: '#71717a', display: 'flex', alignItems: 'center', gap: 4 }}>
                <Calendar size={13} /> Release Date
              </span>
              <p style={{ fontWeight: 600, fontSize: '0.85rem', color: '#fff', marginTop: 2 }}>{game.release_date || 'N/A'}</p>
            </div>
          </div>

          {/* Description */}
          <div style={{ marginBottom: '24px' }}>
            <h4 style={{ color: '#fff', marginBottom: '6px', fontSize: '0.95rem' }}>About</h4>
            <p style={{ color: '#a1a1aa', lineHeight: 1.5, fontSize: '0.9rem' }}>{game.description}</p>
          </div>

          {/* Price & Buy Action */}
          <div style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            padding: '16px 20px',
            background: '#141417',
            borderRadius: '10px',
            border: '1px solid #27272a',
            marginBottom: '28px'
          }}>
            <div>
              <span style={{ fontSize: '0.75rem', color: '#71717a', display: 'block' }}>Price</span>
              {game.discount_percent > 0 ? (
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span style={{ fontSize: '1.3rem', fontWeight: 700, color: '#fff' }}>₹{game.final_price.toFixed(2)}</span>
                  <span style={{ fontSize: '0.85rem', textDecoration: 'line-through', color: '#71717a' }}>₹{game.original_price.toFixed(2)}</span>
                </div>
              ) : (
                <span style={{ fontSize: '1.3rem', fontWeight: 700, color: '#fff' }}>₹{game.final_price.toFixed(2)}</span>
              )}
            </div>

            <div style={{ display: 'flex', gap: '10px' }}>
              <button
                onClick={() => onToggleWishlist(game)}
                className="btn btn-secondary"
              >
                <Heart size={15} fill={isWishlisted ? '#ffffff' : 'none'} color={isWishlisted ? '#ffffff' : 'currentColor'} />
                {isWishlisted ? 'Wishlisted' : 'Wishlist'}
              </button>

              {isOwned ? (
                <button className="btn btn-accent" disabled style={{ opacity: 0.8 }}>
                  <Check size={15} /> In Library
                </button>
              ) : (
                <button onClick={() => onAddToCart(game)} className="btn btn-primary">
                  <ShoppingBag size={15} /> Add to Cart
                </button>
              )}
            </div>
          </div>

          {/* Reviews Section */}
          <div>
            <h4 style={{ color: '#fff', marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.95rem' }}>
              <MessageSquare size={16} /> Community Reviews
            </h4>

            {/* Review Form (if owned) */}
            {isOwned ? (
              <form onSubmit={handleReviewSubmit} style={{
                background: '#141417',
                padding: '14px',
                borderRadius: '8px',
                marginBottom: '16px',
                border: '1px solid #27272a'
              }}>
                <span style={{ fontSize: '0.8rem', fontWeight: 600, color: '#fff', display: 'block', marginBottom: '6px' }}>Write a Review</span>
                
                <div style={{ display: 'flex', gap: '4px', marginBottom: '10px' }}>
                  {[1, 2, 3, 4, 5].map((star) => (
                    <Star
                      key={star}
                      size={18}
                      onClick={() => setRating(star)}
                      style={{
                        cursor: 'pointer',
                        fill: star <= rating ? '#ffffff' : 'none',
                        color: star <= rating ? '#ffffff' : '#3f3f46'
                      }}
                    />
                  ))}
                </div>

                <textarea
                  rows={2}
                  placeholder="Share your experience..."
                  value={comment}
                  onChange={(e) => setComment(e.target.value)}
                  style={{
                    width: '100%',
                    padding: '8px 12px',
                    borderRadius: '6px',
                    background: '#09090b',
                    border: '1px solid #27272a',
                    color: '#fff',
                    outline: 'none',
                    fontSize: '0.85rem',
                    marginBottom: '10px'
                  }}
                />

                <button type="submit" disabled={submitting} className="btn btn-primary" style={{ padding: '6px 12px', fontSize: '0.8rem' }}>
                  <Send size={12} /> Post Review
                </button>
              </form>
            ) : (
              <p style={{ fontSize: '0.8rem', color: '#71717a', fontStyle: 'italic', marginBottom: '12px' }}>
                You must own this game in your library to post a review.
              </p>
            )}

            {/* Reviews List */}
            {game.reviews && game.reviews.length > 0 ? (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                {game.reviews.map((rev, idx) => (
                  <div key={idx} style={{
                    padding: '12px',
                    borderRadius: '8px',
                    background: '#141417',
                    border: '1px solid #27272a'
                  }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
                      <span style={{ fontWeight: 600, fontSize: '0.85rem', color: '#fff' }}>{rev.Username}</span>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '2px' }}>
                        {[...Array(rev.Rating)].map((_, i) => (
                          <Star key={i} size={11} style={{ fill: '#ffffff', color: '#ffffff' }} />
                        ))}
                      </div>
                    </div>
                    <p style={{ color: '#a1a1aa', fontSize: '0.85rem' }}>{rev.Comment}</p>
                  </div>
                ))}
              </div>
            ) : (
              <p style={{ color: '#71717a', fontSize: '0.85rem' }}>No reviews yet.</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

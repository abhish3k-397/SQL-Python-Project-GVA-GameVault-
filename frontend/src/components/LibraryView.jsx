import React, { useState } from 'react';
import { Play, Clock, Calendar, CheckCircle2, Gamepad2 } from 'lucide-react';

export default function LibraryView({ library, onPlayGame }) {
  const [playingId, setPlayingId] = useState(null);

  const handlePlayClick = async (gameId) => {
    setPlayingId(gameId);
    await onPlayGame(gameId, 1.5);
    setTimeout(() => setPlayingId(null), 1200);
  };

  if (!library || library.length === 0) {
    return (
      <div style={{ textAlign: 'center', padding: '80px 20px', color: '#71717a' }}>
        <Gamepad2 size={56} style={{ opacity: 0.3, marginBottom: '16px' }} />
        <h2 style={{ color: '#fff', marginBottom: '8px' }}>Your Library is Empty</h2>
        <p>Purchased games will appear here.</p>
      </div>
    );
  }

  return (
    <div>
      <div style={{ marginBottom: '24px' }}>
        <h2 style={{ fontSize: '1.6rem', color: '#fff', marginBottom: '4px' }}>My Library</h2>
        <p style={{ color: '#a1a1aa', fontSize: '0.9rem' }}>{library.length} titles owned</p>
      </div>

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(260px, 1fr))',
        gap: '20px'
      }}>
        {library.map((game) => (
          <div key={game.game_id} className="glass-panel" style={{ overflow: 'hidden', background: '#121215', border: '1px solid #27272a' }}>
            <div style={{ position: 'relative', height: '160px' }}>
              <img
                src={game.cover_image}
                alt={game.title}
                style={{ width: '100%', height: '100%', objectFit: 'cover', filter: 'grayscale(30%)' }}
              />
              <div style={{
                position: 'absolute',
                inset: 0,
                background: 'linear-gradient(0deg, #121215 0%, transparent 60%)'
              }} />
              <div style={{ position: 'absolute', bottom: '10px', left: '12px' }}>
                <span className="badge badge-genre">{game.age_rating || 'M'}</span>
              </div>
            </div>

            <div style={{ padding: '16px' }}>
              <h3 style={{ fontSize: '1rem', color: '#fff', marginBottom: '8px' }}>{game.title}</h3>

              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '14px', fontSize: '0.8rem', color: '#a1a1aa' }}>
                <span style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
                  <Clock size={13} /> {game.hours_played.toFixed(1)} hrs
                </span>
                <span style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
                  <Calendar size={13} /> {game.purchase_date || 'Owned'}
                </span>
              </div>

              <button
                onClick={() => handlePlayClick(game.game_id)}
                className={`btn ${playingId === game.game_id ? 'btn-secondary' : 'btn-primary'}`}
                style={{ width: '100%', padding: '8px', fontSize: '0.85rem' }}
              >
                {playingId === game.game_id ? (
                  <>
                    <CheckCircle2 size={15} /> Launching...
                  </>
                ) : (
                  <>
                    <Play size={15} /> Play Title
                  </>
                )}
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

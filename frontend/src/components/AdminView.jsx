import React, { useState, useEffect } from 'react';
import { ShieldCheck, Users, Gamepad2, ShoppingBag, DollarSign, PlusCircle, TrendingUp } from 'lucide-react';

export default function AdminView({ onAddGame }) {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  // New Game Form
  const [title, setTitle] = useState('');
  const [price, setPrice] = useState('1999');
  const [description, setDescription] = useState('');
  const [coverImage, setCoverImage] = useState('');
  const [ageRating, setAgeRating] = useState('M');
  const [adding, setAdding] = useState(false);
  const [msg, setMsg] = useState('');

  const fetchStats = async () => {
    try {
      const res = await fetch('/api/admin/stats');
      const data = await res.json();
      setStats(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStats();
  }, []);

  const handleAddGameSubmit = async (e) => {
    e.preventDefault();
    if (!title || !price) return;
    setAdding(true);
    const success = await onAddGame({
      title,
      price: parseFloat(price),
      description,
      age_rating: ageRating,
      cover_image: coverImage || 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=800&q=80'
    });

    if (success) {
      setMsg('Game added successfully!');
      setTitle('');
      setDescription('');
      setCoverImage('');
      fetchStats();
      setTimeout(() => setMsg(''), 3000);
    }
    setAdding(false);
  };

  if (loading) return <div style={{ color: '#fff', textAlign: 'center', padding: '40px' }}>Loading dashboard...</div>;

  return (
    <div>
      <div style={{ marginBottom: '24px' }}>
        <h2 style={{ fontSize: '1.6rem', color: '#fff', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <ShieldCheck size={24} /> Admin Dashboard
        </h2>
        <p style={{ color: '#a1a1aa', fontSize: '0.9rem' }}>Catalog Management & Sales Analytics</p>
      </div>

      {/* Analytics Grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
        gap: '16px',
        marginBottom: '32px'
      }}>
        <div className="glass-panel" style={{ padding: '18px', background: '#121215', border: '1px solid #27272a' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', color: '#a1a1aa' }}>
            <span style={{ fontSize: '0.8rem', fontWeight: 600, color: '#71717a' }}>Total Revenue</span>
            <DollarSign size={18} />
          </div>
          <h2 style={{ fontSize: '1.6rem', color: '#fff', marginTop: '6px' }}>
            ₹{(stats?.total_revenue || 0).toFixed(2)}
          </h2>
        </div>

        <div className="glass-panel" style={{ padding: '18px', background: '#121215', border: '1px solid #27272a' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', color: '#a1a1aa' }}>
            <span style={{ fontSize: '0.8rem', fontWeight: 600, color: '#71717a' }}>Total Orders</span>
            <ShoppingBag size={18} />
          </div>
          <h2 style={{ fontSize: '1.6rem', color: '#fff', marginTop: '6px' }}>
            {stats?.total_orders || 0}
          </h2>
        </div>

        <div className="glass-panel" style={{ padding: '18px', background: '#121215', border: '1px solid #27272a' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', color: '#a1a1aa' }}>
            <span style={{ fontSize: '0.8rem', fontWeight: 600, color: '#71717a' }}>Users</span>
            <Users size={18} />
          </div>
          <h2 style={{ fontSize: '1.6rem', color: '#fff', marginTop: '6px' }}>
            {stats?.total_users || 0}
          </h2>
        </div>

        <div className="glass-panel" style={{ padding: '18px', background: '#121215', border: '1px solid #27272a' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', color: '#a1a1aa' }}>
            <span style={{ fontSize: '0.8rem', fontWeight: 600, color: '#71717a' }}>Catalog</span>
            <Gamepad2 size={18} />
          </div>
          <h2 style={{ fontSize: '1.6rem', color: '#fff', marginTop: '6px' }}>
            {stats?.total_games || 0}
          </h2>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>
        {/* Top Selling Games */}
        <div className="glass-panel" style={{ padding: '20px', background: '#121215', border: '1px solid #27272a' }}>
          <h3 style={{ fontSize: '1.1rem', color: '#fff', marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <TrendingUp size={16} /> Top Titles
          </h3>

          {stats?.top_games && stats.top_games.length > 0 ? (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              {stats.top_games.map((g, idx) => (
                <div key={idx} style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  padding: '10px 14px',
                  background: '#141417',
                  borderRadius: '6px',
                  border: '1px solid #27272a'
                }}>
                  <span style={{ fontWeight: 600, color: '#fff', fontSize: '0.9rem' }}>{g.Title}</span>
                  <span style={{ color: '#a1a1aa', fontWeight: 600, fontSize: '0.85rem' }}>
                    {g.SalesCount} sales (₹{g.Revenue.toFixed(2)})
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <p style={{ color: '#71717a', fontSize: '0.85rem' }}>No orders yet.</p>
          )}
        </div>

        {/* Add New Game Form */}
        <div className="glass-panel" style={{ padding: '20px', background: '#121215', border: '1px solid #27272a' }}>
          <h3 style={{ fontSize: '1.1rem', color: '#fff', marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <PlusCircle size={16} /> Add Game
          </h3>

          {msg && (
            <div style={{ background: '#18181b', color: '#fff', border: '1px solid #3f3f46', padding: '8px 12px', borderRadius: '6px', marginBottom: '12px', fontSize: '0.8rem' }}>
              {msg}
            </div>
          )}

          <form onSubmit={handleAddGameSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            <div>
              <label style={{ fontSize: '0.75rem', color: '#71717a' }}>Title</label>
              <input
                type="text"
                required
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="Game title"
                style={{
                  width: '100%',
                  padding: '8px 12px',
                  borderRadius: '6px',
                  background: '#09090b',
                  border: '1px solid #27272a',
                  color: '#fff',
                  outline: 'none',
                  fontSize: '0.85rem'
                }}
              />
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
              <div>
                <label style={{ fontSize: '0.75rem', color: '#71717a' }}>Price (₹)</label>
                <input
                  type="number"
                  required
                  value={price}
                  onChange={(e) => setPrice(e.target.value)}
                  style={{
                    width: '100%',
                    padding: '8px 12px',
                    borderRadius: '6px',
                    background: '#09090b',
                    border: '1px solid #27272a',
                    color: '#fff',
                    outline: 'none',
                    fontSize: '0.85rem'
                  }}
                />
              </div>

              <div>
                <label style={{ fontSize: '0.75rem', color: '#71717a' }}>Age Rating</label>
                <select
                  value={ageRating}
                  onChange={(e) => setAgeRating(e.target.value)}
                  style={{
                    width: '100%',
                    padding: '8px 12px',
                    borderRadius: '6px',
                    background: '#09090b',
                    border: '1px solid #27272a',
                    color: '#fff',
                    outline: 'none',
                    fontSize: '0.85rem'
                  }}
                >
                  <option value="E">E (Everyone)</option>
                  <option value="T">T (Teen)</option>
                  <option value="M">M (Mature)</option>
                </select>
              </div>
            </div>

            <div>
              <label style={{ fontSize: '0.75rem', color: '#71717a' }}>Image URL</label>
              <input
                type="url"
                value={coverImage}
                onChange={(e) => setCoverImage(e.target.value)}
                placeholder="https://..."
                style={{
                  width: '100%',
                  padding: '8px 12px',
                  borderRadius: '6px',
                  background: '#09090b',
                  border: '1px solid #27272a',
                  color: '#fff',
                  outline: 'none',
                  fontSize: '0.85rem'
                }}
              />
            </div>

            <div>
              <label style={{ fontSize: '0.75rem', color: '#71717a' }}>Description</label>
              <textarea
                rows={2}
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Description"
                style={{
                  width: '100%',
                  padding: '8px 12px',
                  borderRadius: '6px',
                  background: '#09090b',
                  border: '1px solid #27272a',
                  color: '#fff',
                  outline: 'none',
                  fontSize: '0.85rem'
                }}
              />
            </div>

            <button
              type="submit"
              disabled={adding}
              className="btn btn-primary"
              style={{ padding: '10px', fontSize: '0.85rem', marginTop: '4px' }}
            >
              {adding ? 'Publishing...' : 'Publish Game'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

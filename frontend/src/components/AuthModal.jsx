import React, { useState } from 'react';
import { X, User, Lock, Mail, Globe } from 'lucide-react';

export default function AuthModal({ isOpen, onClose, onLogin, onRegister }) {
  const [isRegistering, setIsRegistering] = useState(false);
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [country, setCountry] = useState('India');
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg('');
    setLoading(true);

    if (isRegistering) {
      const res = await onRegister(username, email, password, country);
      if (res.error) setErrorMsg(res.error);
      else onClose();
    } else {
      const res = await onLogin(username, password);
      if (res.error) setErrorMsg(res.error);
      else onClose();
    }
    setLoading(false);
  };

  const handleDemoClick = (demoUser, demoPass) => {
    setUsername(demoUser);
    setPassword(demoPass);
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-card" onClick={(e) => e.stopPropagation()} style={{ maxWidth: '400px', padding: '24px', background: '#0f0f12', border: '1px solid #27272a' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <div>
            <h3 style={{ fontSize: '1.3rem', color: '#fff' }}>
              {isRegistering ? 'Create Account' : 'Sign In'}
            </h3>
            <p style={{ color: '#71717a', fontSize: '0.8rem', marginTop: 2 }}>
              {isRegistering ? 'Sign up & get ₹500 welcome credit' : 'Access your GameVault library'}
            </p>
          </div>
          <button onClick={onClose} className="btn btn-ghost btn-icon"><X size={16} /></button>
        </div>

        {errorMsg && (
          <div style={{
            background: '#18181b',
            border: '1px solid #3f3f46',
            color: '#ffffff',
            padding: '8px 12px',
            borderRadius: '6px',
            fontSize: '0.8rem',
            marginBottom: '14px'
          }}>
            {errorMsg}
          </div>
        )}

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          <div>
            <label style={{ fontSize: '0.75rem', color: '#71717a', display: 'block', marginBottom: 4 }}>Username or Email</label>
            <div style={{ position: 'relative' }}>
              <User size={15} style={{ position: 'absolute', left: 10, top: '50%', transform: 'translateY(-50%)', color: '#71717a' }} />
              <input
                type="text"
                required
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="e.g. arjun_92"
                style={{
                  width: '100%',
                  padding: '8px 12px 8px 34px',
                  borderRadius: '6px',
                  background: '#09090b',
                  border: '1px solid #27272a',
                  color: '#fff',
                  outline: 'none',
                  fontSize: '0.85rem'
                }}
              />
            </div>
          </div>

          {isRegistering && (
            <>
              <div>
                <label style={{ fontSize: '0.75rem', color: '#71717a', display: 'block', marginBottom: 4 }}>Email Address</label>
                <div style={{ position: 'relative' }}>
                  <Mail size={15} style={{ position: 'absolute', left: 10, top: '50%', transform: 'translateY(-50%)', color: '#71717a' }} />
                  <input
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="name@example.com"
                    style={{
                      width: '100%',
                      padding: '8px 12px 8px 34px',
                      borderRadius: '6px',
                      background: '#09090b',
                      border: '1px solid #27272a',
                      color: '#fff',
                      outline: 'none',
                      fontSize: '0.85rem'
                    }}
                  />
                </div>
              </div>

              <div>
                <label style={{ fontSize: '0.75rem', color: '#71717a', display: 'block', marginBottom: 4 }}>Country</label>
                <div style={{ position: 'relative' }}>
                  <Globe size={15} style={{ position: 'absolute', left: 10, top: '50%', transform: 'translateY(-50%)', color: '#71717a' }} />
                  <input
                    type="text"
                    value={country}
                    onChange={(e) => setCountry(e.target.value)}
                    placeholder="India"
                    style={{
                      width: '100%',
                      padding: '8px 12px 8px 34px',
                      borderRadius: '6px',
                      background: '#09090b',
                      border: '1px solid #27272a',
                      color: '#fff',
                      outline: 'none',
                      fontSize: '0.85rem'
                    }}
                  />
                </div>
              </div>
            </>
          )}

          <div>
            <label style={{ fontSize: '0.75rem', color: '#71717a', display: 'block', marginBottom: 4 }}>Password</label>
            <div style={{ position: 'relative' }}>
              <Lock size={15} style={{ position: 'absolute', left: 10, top: '50%', transform: 'translateY(-50%)', color: '#71717a' }} />
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                style={{
                  width: '100%',
                  padding: '8px 12px 8px 34px',
                  borderRadius: '6px',
                  background: '#09090b',
                  border: '1px solid #27272a',
                  color: '#fff',
                  outline: 'none',
                  fontSize: '0.85rem'
                }}
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="btn btn-primary"
            style={{ width: '100%', padding: '10px', fontSize: '0.9rem', marginTop: '6px' }}
          >
            {loading ? 'Authenticating...' : (isRegistering ? 'Create Account' : 'Sign In')}
          </button>
        </form>

        {/* Demo Accounts Quick Login */}
        <div style={{
          marginTop: '20px',
          paddingTop: '14px',
          borderTop: '1px solid #27272a',
          textAlign: 'center'
        }}>
          <span style={{ fontSize: '0.75rem', color: '#71717a', display: 'block', marginBottom: '8px' }}>
            Quick Demo Credentials
          </span>
          <div style={{ display: 'flex', gap: '8px', justifyContent: 'center' }}>
            <button
              onClick={() => handleDemoClick('arjun_92', 'hash1')}
              className="btn btn-secondary"
              style={{ fontSize: '0.75rem', padding: '4px 10px' }}
            >
              User: arjun_92
            </button>
            <button
              onClick={() => handleDemoClick('admin', 'admin123')}
              className="btn btn-secondary"
              style={{ fontSize: '0.75rem', padding: '4px 10px' }}
            >
              Admin: admin
            </button>
          </div>
        </div>

        <div style={{ textAlign: 'center', marginTop: '14px' }}>
          <button
            type="button"
            onClick={() => { setIsRegistering(!isRegistering); setErrorMsg(''); }}
            style={{ background: 'none', border: 'none', color: '#ffffff', fontSize: '0.8rem', cursor: 'pointer', textDecoration: 'underline' }}
          >
            {isRegistering ? 'Already have an account? Sign in' : "Need an account? Sign up"}
          </button>
        </div>
      </div>
    </div>
  );
}

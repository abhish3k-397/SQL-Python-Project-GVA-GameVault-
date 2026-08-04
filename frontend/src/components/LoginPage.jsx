import React, { useState } from 'react';
import { Gamepad2, User, Lock, Mail, Globe, ArrowRight, ShieldCheck, CheckCircle2 } from 'lucide-react';

export default function LoginPage({ onLogin, onRegister, onSelectTab }) {
  const [isRegistering, setIsRegistering] = useState(false);
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [country, setCountry] = useState('India');
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg('');
    setLoading(true);

    if (isRegistering) {
      const res = await onRegister(username, email, password, country);
      if (res.error) setErrorMsg(res.error);
      else onSelectTab('store');
    } else {
      const res = await onLogin(username, password);
      if (res.error) setErrorMsg(res.error);
      else onSelectTab('store');
    }
    setLoading(false);
  };

  const handleDemoClick = (demoUser, demoPass) => {
    setUsername(demoUser);
    setPassword(demoPass);
  };

  return (
    <div style={{
      minHeight: '75vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '24px 12px'
    }}>
      <div className="glass-panel" style={{
        width: '100%',
        maxWidth: '420px',
        padding: '32px 28px',
        background: '#0f0f12',
        border: '1px solid #1f1f23',
        borderRadius: '12px'
      }}>
        {/* Brand Header */}
        <div style={{ textAlign: 'center', marginBottom: '24px' }}>
          <div style={{
            width: '40px',
            height: '40px',
            borderRadius: '8px',
            background: '#ffffff',
            display: 'inline-flex',
            alignItems: 'center',
            justifyContent: 'center',
            marginBottom: '12px'
          }}>
            <Gamepad2 size={24} color="#000000" />
          </div>
          <h2 style={{ fontSize: '1.4rem', color: '#ffffff', marginBottom: '4px' }}>
            {isRegistering ? 'Create GameVault Account' : 'Sign in to GameVault'}
          </h2>
          <p style={{ color: '#71717a', fontSize: '12px' }}>
            {isRegistering
              ? 'Get your personal game vault & ₹500 welcome bonus'
              : 'Access your private digital library and wishlist'}
          </p>
        </div>

        {/* Error Alert */}
        {errorMsg && (
          <div style={{
            background: '#18181b',
            border: '1px solid #3f3f46',
            color: '#ffffff',
            padding: '8px 12px',
            borderRadius: '6px',
            fontSize: '12px',
            marginBottom: '16px',
            textAlign: 'center'
          }}>
            {errorMsg}
          </div>
        )}

        {/* Auth Form */}
        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          <div>
            <label style={{ fontSize: '11px', color: '#71717a', display: 'block', marginBottom: 4 }}>Username or Email</label>
            <div style={{ position: 'relative' }}>
              <User size={14} style={{ position: 'absolute', left: 10, top: '50%', transform: 'translateY(-50%)', color: '#52525b' }} />
              <input
                type="text"
                required
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Username or email"
                style={{
                  width: '100%',
                  padding: '8px 12px 8px 32px',
                  borderRadius: '6px',
                  background: '#09090b',
                  border: '1px solid #1f1f23',
                  color: '#fff',
                  outline: 'none',
                  fontSize: '12px'
                }}
              />
            </div>
          </div>

          {isRegistering && (
            <>
              <div>
                <label style={{ fontSize: '11px', color: '#71717a', display: 'block', marginBottom: 4 }}>Email Address</label>
                <div style={{ position: 'relative' }}>
                  <Mail size={14} style={{ position: 'absolute', left: 10, top: '50%', transform: 'translateY(-50%)', color: '#52525b' }} />
                  <input
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="name@example.com"
                    style={{
                      width: '100%',
                      padding: '8px 12px 8px 32px',
                      borderRadius: '6px',
                      background: '#09090b',
                      border: '1px solid #1f1f23',
                      color: '#fff',
                      outline: 'none',
                      fontSize: '12px'
                    }}
                  />
                </div>
              </div>

              <div>
                <label style={{ fontSize: '11px', color: '#71717a', display: 'block', marginBottom: 4 }}>Country</label>
                <div style={{ position: 'relative' }}>
                  <Globe size={14} style={{ position: 'absolute', left: 10, top: '50%', transform: 'translateY(-50%)', color: '#52525b' }} />
                  <input
                    type="text"
                    value={country}
                    onChange={(e) => setCountry(e.target.value)}
                    placeholder="India"
                    style={{
                      width: '100%',
                      padding: '8px 12px 8px 32px',
                      borderRadius: '6px',
                      background: '#09090b',
                      border: '1px solid #1f1f23',
                      color: '#fff',
                      outline: 'none',
                      fontSize: '12px'
                    }}
                  />
                </div>
              </div>
            </>
          )}

          <div>
            <label style={{ fontSize: '11px', color: '#71717a', display: 'block', marginBottom: 4 }}>Password</label>
            <div style={{ position: 'relative' }}>
              <Lock size={14} style={{ position: 'absolute', left: 10, top: '50%', transform: 'translateY(-50%)', color: '#52525b' }} />
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                style={{
                  width: '100%',
                  padding: '8px 12px 8px 32px',
                  borderRadius: '6px',
                  background: '#09090b',
                  border: '1px solid #1f1f23',
                  color: '#fff',
                  outline: 'none',
                  fontSize: '12px'
                }}
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="btn btn-primary"
            style={{ width: '100%', padding: '9px', fontSize: '12px', marginTop: '6px' }}
          >
            {loading ? 'Authenticating...' : (isRegistering ? 'Create Account' : 'Sign In')}
            <ArrowRight size={13} />
          </button>
        </form>

        {/* Demo Accounts Quick Login */}
        <div style={{
          marginTop: '20px',
          paddingTop: '16px',
          borderTop: '1px solid #1f1f23',
          textAlign: 'center'
        }}>
          <span style={{ fontSize: '10px', color: '#52525b', display: 'block', marginBottom: '8px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            Quick Demo Accounts
          </span>
          <div style={{ display: 'flex', gap: '6px', justifyContent: 'center', flexWrap: 'wrap' }}>
            <button
              onClick={() => handleDemoClick('arjun_92', 'hash1')}
              className="btn btn-secondary"
              style={{ fontSize: '11px', padding: '4px 8px' }}
            >
              arjun_92
            </button>
            <button
              onClick={() => handleDemoClick('sara_k', 'hash2')}
              className="btn btn-secondary"
              style={{ fontSize: '11px', padding: '4px 8px' }}
            >
              sara_k
            </button>
            <button
              onClick={() => handleDemoClick('admin', 'admin123')}
              className="btn btn-secondary"
              style={{ fontSize: '11px', padding: '4px 8px', borderColor: '#3f3f46' }}
            >
              admin
            </button>
          </div>
        </div>

        {/* Mode Toggle */}
        <div style={{ textAlign: 'center', marginTop: '16px' }}>
          <button
            type="button"
            onClick={() => { setIsRegistering(!isRegistering); setErrorMsg(''); }}
            style={{ background: 'none', border: 'none', color: '#ffffff', fontSize: '12px', cursor: 'pointer', textDecoration: 'underline' }}
          >
            {isRegistering ? 'Already have an account? Sign in' : "Don't have an account? Sign up"}
          </button>
        </div>
      </div>
    </div>
  );
}

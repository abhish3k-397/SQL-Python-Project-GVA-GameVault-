import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import Navbar from './components/Navbar';
import HeroBanner from './components/HeroBanner';
import GameCard from './components/GameCard';
import GameDetailModal from './components/GameDetailModal';
import CartDrawer from './components/CartDrawer';
import LibraryView from './components/LibraryView';
import WishlistView from './components/WishlistView';
import WalletModal from './components/WalletModal';
import LoginPage from './components/LoginPage';
import AdminView from './components/AdminView';
import Toast from './components/Toast';
import { Filter, SortAsc } from 'lucide-react';

export default function App() {
  // State Management
  const [user, setUser] = useState(null);
  const [activeTab, setActiveTab] = useState('store'); // 'store' | 'library' | 'wishlist' | 'admin' | 'login'

  const [games, setGames] = useState([]);
  const [genres, setGenres] = useState([]);
  const [selectedGenre, setSelectedGenre] = useState('');
  const [selectedSort, setSelectedSort] = useState('');
  const [searchQuery, setSearchQuery] = useState('');

  const [selectedGame, setSelectedGame] = useState(null);
  const [cart, setCart] = useState([]);
  const [library, setLibrary] = useState([]);
  const [wishlist, setWishlist] = useState([]);

  // Modals & Drawers
  const [isCartOpen, setIsCartOpen] = useState(false);
  const [isWalletOpen, setIsWalletOpen] = useState(false);

  // Toast
  const [toast, setToast] = useState(null);

  const showToast = (message, type = 'success') => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 3500);
  };

  // Fetch Games & Genres
  const fetchGames = async () => {
    try {
      const query = new URLSearchParams();
      if (selectedGenre) query.append('genre', selectedGenre);
      if (selectedSort) query.append('sort', selectedSort);
      if (searchQuery) query.append('search', searchQuery);

      const res = await fetch(`/api/games?${query.toString()}`);
      const data = await res.json();
      if (Array.isArray(data)) {
        setGames(data);
      } else {
        setGames([]);
      }
    } catch (err) {
      console.error('Error fetching games:', err);
      setGames([]);
    }
  };

  const fetchGenres = async () => {
    try {
      const res = await fetch('/api/genres');
      const data = await res.json();
      setGenres(data);
    } catch (err) {
      console.error('Error fetching genres:', err);
    }
  };

  // User Data loader — ISOLATED per user_id!
  const fetchUserData = async (userId) => {
    if (userId === undefined || userId === null) {
      setLibrary([]);
      setWishlist([]);
      return;
    }
    try {
      // Library
      const libRes = await fetch(`/api/user/library?user_id=${userId}`);
      const libData = await libRes.json();
      if (Array.isArray(libData)) setLibrary(libData);
      else setLibrary([]);

      // Wishlist
      const wishRes = await fetch(`/api/user/wishlist?user_id=${userId}`);
      const wishData = await wishRes.json();
      if (Array.isArray(wishData)) setWishlist(wishData);
      else setWishlist([]);
    } catch (err) {
      console.error('Error loading user data:', err);
      setLibrary([]);
      setWishlist([]);
    }
  };

  useEffect(() => {
    fetchGames();
  }, [selectedGenre, selectedSort, searchQuery]);

  useEffect(() => {
    fetchGenres();
    // Load saved session if exists (DO NOT auto-login as demo user!)
    const savedUser = localStorage.getItem('gv_user');
    if (savedUser) {
      try {
        const parsed = JSON.parse(savedUser);
        if (parsed && parsed.user_id !== undefined) {
          setUser(parsed);
          fetchUserData(parsed.user_id);
        }
      } catch (e) {
        localStorage.removeItem('gv_user');
      }
    }
  }, []);

  // Handlers
  const handleLogin = async (username, password) => {
    try {
      const res = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });
      const data = await res.json();
      if (res.ok) {
        setUser(data.user);
        localStorage.setItem('gv_user', JSON.stringify(data.user));
        fetchUserData(data.user.user_id);
        showToast(`Signed in as ${data.user.username}`);
        return { success: true };
      } else {
        return { error: data.error };
      }
    } catch (err) {
      return { error: 'Network error connecting to API' };
    }
  };

  const handleRegister = async (username, email, password, country) => {
    try {
      const res = await fetch('/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email, password, country })
      });
      const data = await res.json();
      if (res.ok) {
        setUser(data.user);
        localStorage.setItem('gv_user', JSON.stringify(data.user));
        fetchUserData(data.user.user_id);
        showToast(data.message);
        return { success: true };
      } else {
        return { error: data.error };
      }
    } catch (err) {
      return { error: 'Registration failed' };
    }
  };

  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem('gv_user');
    setLibrary([]);
    setWishlist([]);
    setCart([]);
    setActiveTab('store');
    showToast('Signed out of GameVault.', 'info');
  };

  // Cart
  const handleAddToCart = (game) => {
    if (cart.some(i => i.game_id === game.game_id)) {
      showToast(`${game.title} is already in your cart.`, 'info');
      return;
    }
    if (library.some(i => i.game_id === game.game_id)) {
      showToast(`You already own ${game.title} in your Library!`, 'error');
      return;
    }
    setCart([...cart, game]);
    showToast(`Added ${game.title} to cart.`);
  };

  const handleRemoveFromCart = (gameId) => {
    setCart(cart.filter(i => i.game_id !== gameId));
  };

  // Wishlist
  const handleToggleWishlist = async (game) => {
    if (!user) {
      setActiveTab('login');
      showToast('Please sign in to save titles to your wishlist', 'info');
      return;
    }

    const isWish = wishlist.some(w => w.game_id === game.game_id);
    if (isWish) {
      await fetch(`/api/user/wishlist?user_id=${user.user_id}&game_id=${game.game_id}`, { method: 'DELETE' });
      setWishlist(wishlist.filter(w => w.game_id !== game.game_id));
      showToast(`Removed ${game.title} from Wishlist`, 'info');
    } else {
      await fetch('/api/user/wishlist', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: user.user_id, game_id: game.game_id })
      });
      setWishlist([...wishlist, game]);
      showToast(`Saved ${game.title} to Wishlist!`);
    }
  };

  // Checkout
  const handleCheckout = async (gameIds, paymentMethod) => {
    if (!user) {
      setIsCartOpen(false);
      setActiveTab('login');
      showToast('Please sign in to complete your checkout', 'info');
      return;
    }

    try {
      const res = await fetch('/api/user/checkout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: user.user_id,
          game_ids: gameIds,
          payment_method: paymentMethod
        })
      });
      const data = await res.json();

      if (res.ok) {
        setUser({ ...user, wallet_balance: data.updated_wallet_balance });
        localStorage.setItem('gv_user', JSON.stringify({ ...user, wallet_balance: data.updated_wallet_balance }));
        setCart([]);
        setIsCartOpen(false);
        fetchUserData(user.user_id);
        showToast(data.message);
      } else {
        showToast(data.error || 'Checkout failed', 'error');
      }
    } catch (err) {
      showToast('Checkout network error', 'error');
    }
  };

  // Deposit
  const handleDeposit = async (amount) => {
    if (!user) return;

    try {
      const res = await fetch('/api/user/wallet/deposit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: user.user_id, amount })
      });
      const data = await res.json();

      if (res.ok) {
        const updated = { ...user, wallet_balance: data.updated_wallet_balance };
        setUser(updated);
        localStorage.setItem('gv_user', JSON.stringify(updated));
        showToast(data.message);
      } else {
        showToast(data.error, 'error');
      }
    } catch (err) {
      showToast('Deposit failed', 'error');
    }
  };

  // Play game
  const handlePlayGame = async (gameId, hours) => {
    if (!user) return;
    await fetch('/api/user/library/play', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: user.user_id, game_id: gameId, hours })
    });
    fetchUserData(user.user_id);
  };

  // Submit Review
  const handleSubmitReview = async (gameId, rating, comment) => {
    if (!user) return;
    try {
      const res = await fetch('/api/reviews', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: user.user_id, game_id: gameId, rating, comment })
      });
      const data = await res.json();
      if (res.ok) {
        showToast(data.message);
        const gRes = await fetch(`/api/games/${gameId}`);
        const gData = await gRes.json();
        setSelectedGame(gData);
        fetchGames();
      } else {
        showToast(data.error, 'error');
      }
    } catch (err) {
      showToast('Failed to post review', 'error');
    }
  };

  // Admin Add Game
  const handleAddGame = async (gameData) => {
    try {
      const res = await fetch('/api/admin/games', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(gameData)
      });
      if (res.ok) {
        fetchGames();
        showToast('New game title published!');
        return true;
      }
    } catch (err) {
      showToast('Error adding game', 'error');
    }
    return false;
  };

  const featuredGame = games.find(g => g.game_id === 1) || games[0];

  return (
    <div className="app-layout">
      {/* Left Sidebar Navigation */}
      <Sidebar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        selectedGenre={selectedGenre}
        setSelectedGenre={setSelectedGenre}
        genres={genres}
        user={user}
        cartCount={cart.length}
        wishlistCount={wishlist.length}
        onOpenCart={() => setIsCartOpen(true)}
        onOpenWallet={() => setIsWalletOpen(true)}
        onLogout={handleLogout}
      />

      {/* Main Wrapper */}
      <div className="main-wrapper">
        {/* Top Navbar */}
        <Navbar
          user={user}
          cartCount={cart.length}
          searchQuery={searchQuery}
          setSearchQuery={setSearchQuery}
          onOpenCart={() => setIsCartOpen(true)}
          onOpenWallet={() => setIsWalletOpen(true)}
          onNavigateLogin={() => setActiveTab('login')}
        />

        {/* Content Body */}
        <main className="main-content">
          {activeTab === 'store' && (
            <>
              {/* Hero Banner */}
              {!searchQuery && !selectedGenre && (
                <HeroBanner
                  game={featuredGame}
                  onSelectGame={(g) => setSelectedGame(g)}
                  onAddToCart={handleAddToCart}
                />
              )}

              {/* Filter Controls Bar */}
              <div style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                marginBottom: '20px',
                gap: '12px'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span style={{ fontSize: '11px', color: '#52525b', textTransform: 'uppercase', fontWeight: 700, letterSpacing: '0.05em' }}>
                    {selectedGenre ? `Genre: ${selectedGenre}` : 'Catalog (All Games)'}
                  </span>
                  {selectedGenre && (
                    <button
                      onClick={() => setSelectedGenre('')}
                      className="btn btn-ghost"
                      style={{ fontSize: '11px', padding: '2px 6px' }}
                    >
                      Reset Filter
                    </button>
                  )}
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <span style={{ fontSize: '11px', color: '#52525b' }}>Sort:</span>
                  <select
                    value={selectedSort}
                    onChange={(e) => setSelectedSort(e.target.value)}
                    style={{
                      background: '#121215',
                      border: '1px solid #1f1f23',
                      color: '#ffffff',
                      padding: '4px 8px',
                      borderRadius: '4px',
                      outline: 'none',
                      fontSize: '11px'
                    }}
                  >
                    <option value="">Featured</option>
                    <option value="price_low">Price: Low to High</option>
                    <option value="price_high">Price: High to Low</option>
                    <option value="rating">Top Rated</option>
                  </select>
                </div>
              </div>

              {/* Games Grid */}
              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fill, minmax(240px, 1fr))',
                gap: '16px'
              }}>
                {games.map(game => (
                  <GameCard
                    key={game.game_id}
                    game={game}
                    isOwned={library.some(l => l.game_id === game.game_id)}
                    isWishlisted={wishlist.some(w => w.game_id === game.game_id)}
                    onSelectGame={async (g) => {
                      const res = await fetch(`/api/games/${g.game_id}`);
                      const detail = await res.json();
                      setSelectedGame(detail);
                    }}
                    onAddToCart={handleAddToCart}
                    onToggleWishlist={handleToggleWishlist}
                  />
                ))}
              </div>
            </>
          )}

          {activeTab === 'login' && (
            <LoginPage
              onLogin={handleLogin}
              onRegister={handleRegister}
              onSelectTab={setActiveTab}
            />
          )}

          {activeTab === 'library' && (
            <LibraryView library={library} onPlayGame={handlePlayGame} />
          )}

          {activeTab === 'wishlist' && (
            <WishlistView
              wishlist={wishlist}
              onAddToCart={handleAddToCart}
              onRemoveFromWishlist={handleToggleWishlist}
              onSelectGame={(g) => setSelectedGame(g)}
            />
          )}

          {activeTab === 'admin' && (
            <AdminView onAddGame={handleAddGame} />
          )}
        </main>
      </div>

      {/* Modals & Overlay Drawers */}
      <GameDetailModal
        game={selectedGame}
        user={user}
        isOwned={library.some(l => l.game_id === selectedGame?.game_id)}
        isWishlisted={wishlist.some(w => w.game_id === selectedGame?.game_id)}
        onClose={() => setSelectedGame(null)}
        onAddToCart={handleAddToCart}
        onToggleWishlist={handleToggleWishlist}
        onSubmitReview={handleSubmitReview}
      />

      <CartDrawer
        isOpen={isCartOpen}
        onClose={() => setIsCartOpen(false)}
        cartItems={cart}
        user={user}
        onRemoveFromCart={handleRemoveFromCart}
        onCheckout={handleCheckout}
        onOpenAuth={() => setActiveTab('login')}
      />

      <WalletModal
        isOpen={isWalletOpen}
        onClose={() => setIsWalletOpen(false)}
        user={user}
        onDeposit={handleDeposit}
      />

      {/* Notification Toast */}
      <Toast toast={toast} onClose={() => setToast(null)} />
    </div>
  );
}

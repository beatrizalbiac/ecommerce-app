import { Link, Outlet } from "react-router-dom";
import { useAuth } from "../context/auth";
import { useCart } from "../context/cart";
import "./Layout.css";

export default function Layout() {
  const { user, logout } = useAuth();
  const { getCartTotal } = useCart();

  const cartTotal = getCartTotal();

  return (
    <div className="layout">
      <header className="header">
        <div className="header-content">
          <Link to="/" className="logo">
            BAECOMMERCE
          </Link>

          <nav className="nav">
            <Link to="/" className="nav-link">Products</Link>
            <Link to="/cart" className="nav-link">
              Cart {cartTotal > 0 && <span className="cart-badge">{cartTotal}</span>}
            </Link>
            {user ? ( /* an if else, to show visually wether the user's logged in or not */
              <>
                <Link to="/orders" className="nav-link">Orders</Link>
                <span className="user-name">Hi, {user.name}!</span>
                <button onClick={logout} className="nav-link logout-btn">Logout</button>
              </>
            ) : (
              <>
                <Link to="/login" className="nav-link">Login</Link>
                <Link to="/register" className="nav-link">Register</Link>
              </>
            )}
          </nav>
        </div>
      </header>

      <main className="main">
        <Outlet />
      </main>

      <footer className="footer">
        <p>© 2026 BAECOMMERCE</p>
      </footer>
    </div>
  );
}
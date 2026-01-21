import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useCart } from "../context/cart";
import { useAuth } from "../context/auth";
import type { Product } from "../models";
import { getProductById } from "../api/products";
import "./Cart.css";

interface CartItemWithProduct {
  product_id: number;
  quantity: number;
  product: Product; // cart only stores ids, so full product info is fetched here for display
}

export default function Cart() {
  const { cart, updateQuantity, removeFromCart } = useCart();
  const { user } = useAuth();
  const navigate = useNavigate();

  const [cartItems, setCartItems] = useState<CartItemWithProduct[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadCartProducts() {
      if (cart.length === 0) {
        setLoading(false);
        return;
      }

      setLoading(true);
      setError(null);

      try {
        const itemsWithProducts = await Promise.all(
          cart.map(async (item) => {
            const product = await getProductById(item.product_id);

            return {
              ...item,
              product,
            };
          })
        );

        setCartItems(itemsWithProducts);
      } catch (err) {
        setError(
          err instanceof Error ? err.message : "Failed to load cart items"
        );
      } finally {
        setLoading(false);
      }
    }

    loadCartProducts();
  }, [cart]);

  const formatPrice = (cents: number) => {
    return `€${(cents / 100).toFixed(2)}`; // prices are stored in cents to avoid float issues
  };

  const calculateItemTotal = (item: CartItemWithProduct) => {
    return item.product.price_cents * item.quantity;
  };

  const calculateCartTotal = () => {
    return cartItems.reduce(
      (total, item) => total + calculateItemTotal(item),
      0
    );
  };

  const handleCheckout = () => {
    if (!user) {
      navigate("/login"); // forces login before checkout
    } else {
      navigate("/checkout");
    }
  };

  if (loading) {
    return <div className="loading">Loading cart...</div>;
  }

  if (error) {
    return <div className="error">Error: {error}</div>;
  }

  if (cart.length === 0) {
    return (
      <div className="empty-cart">
        <h2>Your cart is empty</h2>
        <p>Add some products to get started!</p>
        <Link to="/" className="btn-back">
          Continue Shopping
        </Link>
      </div>
    );
  }

  return (
    <div className="cart-page">
      <h1>Shopping Cart</h1>

      <div className="cart-content">
        <div className="cart-items">
          {cartItems.map((item) => (
            <div key={item.product_id} className="cart-item">
              <Link
                to={`/products/${item.product.slug}`}
                className="cart-item-image">
                <span>📦</span>{/* just to show something, as i'm not going to add actual images for each product */}
              </Link>

              <div className="cart-item-info">
                <Link
                  to={`/products/${item.product.slug}`}
                  className="cart-item-title"
                >
                  {item.product.title}
                </Link>

                <p className="cart-item-price">
                  {formatPrice(item.product.price_cents)} each
                </p>

                {item.quantity > item.product.stock && (
                  <p className="stock-warning">
                    Only {item.product.stock} available in stock
                  </p>
                )}
              </div>

              <div className="cart-item-quantity">
                <button
                  onClick={() =>
                    updateQuantity(item.product_id, item.quantity - 1)
                  }
                  disabled={item.quantity <= 1} // so it doesn't go under 1
                  className="qty-btn"
                >
                  −
                </button>

                <span className="qty-display">{item.quantity}</span>

                <button
                  onClick={() =>
                    updateQuantity(item.product_id, item.quantity + 1)
                  }
                  disabled={item.quantity >= item.product.stock} // to prevent ordering more than the available stock
                  className="qty-btn"
                >
                  +
                </button>
              </div>

              <div className="cart-item-total">
                {formatPrice(calculateItemTotal(item))}
              </div>

              <button
                onClick={() => removeFromCart(item.product_id)}
                className="remove-btn"
                title="Remove item"
              >
                ✕
              </button>
            </div>
          ))}
        </div>

        <div className="cart-summary">
          <h2>Order Summary</h2>

          <div className="summary-row">
            <span>Subtotal ({cart.length} items)</span>
            <span>{formatPrice(calculateCartTotal())}</span>
          </div>

          <div className="summary-row total">
            <span>Total</span>
            <span>{formatPrice(calculateCartTotal())}</span>
          </div>

          <button onClick={handleCheckout} className="checkout-btn">
            {user ? "Proceed to Checkout" : "Login to Checkout"}
          </button>

          <Link to="/" className="continue-shopping">
            ← Continue Shopping
          </Link>
        </div>
      </div>
    </div>
  );
}

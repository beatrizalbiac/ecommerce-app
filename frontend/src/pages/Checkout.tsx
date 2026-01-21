import { useEffect, useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useCart } from "../context/cart";
import { useAuth } from "../context/auth";
import { validateCart } from "../api/cart";
import { createOrder } from "../api/orders";
import type { CartValidationResponse } from "../models";
import "./Checkout.css";

export default function Checkout() {
  const { cart, clearCart } = useCart();
  const { user, token } = useAuth();
  const navigate = useNavigate();

  const [validation, setValidation] = useState<CartValidationResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [creating, setCreating] = useState(false);

  useEffect(() => {
    if (!user) {
      navigate("/login"); // checkout requires authentication
      return;
    }

    if (cart.length === 0) {
      navigate("/cart"); // there's nothing to checkout if cart is empty
      return;
    }

    async function validateCheckout() {
      setLoading(true);
      setError(null);

      try {
        const validationResult = await validateCart(cart);
        setValidation(validationResult);

        if (!validationResult.all_available) {
          setError(
            "Some items in your cart are not available. Please review your cart."
          ); // backend already tells which items fail
        }
      } catch (err) {
        setError(
          err instanceof Error ? err.message : "Failed to validate cart"
        );
      } finally {
        setLoading(false);
      }
    }

    validateCheckout();
  }, [cart, user, navigate]);

  const formatPrice = (cents: number) => {
    return `€${(cents / 100).toFixed(2)}`;
  };

  const handlePlaceOrder = async () => {
    if (!token || !validation?.all_available) return; // extra safety check before sending the order

    setCreating(true);
    setError(null);

    try {
      await createOrder(cart, token); // backend creates the order using the current cart state
      clearCart(); // cart is cleared only after successful order creation
      navigate("/orders"); // redirects to orders history
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to create order"
      );
    } finally {
      setCreating(false);
    }
  };

  if (loading) {
    return <div className="loading">Validating cart...</div>;
  }

  if (!validation) {
    return <div className="error">Failed to load checkout</div>;
  }

  return (
    <div className="checkout-page">
      <h1>Checkout</h1>

      {error && <div className="error-message">{error}</div>}

      <div className="checkout-content">
        <div className="checkout-items">
          <h2>Order Items</h2>

          {validation.items.map((item) => (
            <div
              key={item.product_id}
              className={`checkout-item ${
                !item.available ? "unavailable" : ""
              }`}
            >
              <div className="checkout-item-info">
                <h3>{item.title}</h3>
                <p className="checkout-item-details">
                  {formatPrice(item.price_cents)} × {item.quantity} ={" "}
                  {formatPrice(item.total_price)}
                </p>
              </div>

              <div className="checkout-item-status">
                {!item.available ? (
                  <span className="status-unavailable">
                    ⚠️ Only {item.available_stock} available
                  </span>
                ) : item.available_stock < 5 ? (
                  <span className="status-low-stock">
                    Only {item.available_stock} left
                  </span>
                ) : (
                  <span className="status-available">✓ Available</span>
                )}
              </div>
            </div>
          ))}

          {!validation.all_available && (
            <div className="cart-warning">
              <p>⚠️ Some items are not available with the requested quantity.</p>
              <Link to="/cart" className="update-cart-link">
                Update cart
              </Link>
            </div>
          )}
        </div>

        <div className="checkout-summary">
          <h2>Order Summary</h2>

          <div className="summary-details">
            <div className="summary-row">
              <span>Items ({validation.items.length})</span>
              <span>{validation.items.length}</span>
            </div>

            <div className="summary-row">
              <span>Subtotal</span>
              <span>{formatPrice(validation.total_cents)}</span>
            </div>

            <div className="summary-row total">
              <span>Total</span>
              <span>{formatPrice(validation.total_cents)}</span>
            </div>
          </div>

          <button
            onClick={handlePlaceOrder}
            disabled={!validation.all_available || creating}
            className="place-order-btn"
          >
            {creating ? "Processing..." : "Place Order"}
          </button>

          <Link to="/cart" className="back-to-cart">
            ← Back to cart
          </Link>
        </div>
      </div>
    </div>
  );
}

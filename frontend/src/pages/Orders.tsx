import { useEffect, useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../context/auth";
import { getUserOrders } from "../api/orders";
import type { Order } from "../models";
import "./Orders.css";

export default function Orders() {
  const { user, token } = useAuth();
  const navigate = useNavigate();

  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // if the user is not logged in, there's no point in being here
    if (!user || !token) {
      navigate("/login");
      return;
    }

    async function fetchOrders() {
      setLoading(true);
      setError(null);

      try {
        const data = await getUserOrders(token!);

        // so the most recent orders appear first
        const sortedOrders = data.sort(
          (a, b) =>
            new Date(b.created_at).getTime() -
            new Date(a.created_at).getTime()
        );

        setOrders(sortedOrders);
      } catch (err) {
        setError(
          err instanceof Error ? err.message : "Failed to load orders"
        );
      } finally {
        setLoading(false);
      }
    }

    fetchOrders();
  }, [user, token, navigate]);

  const formatPrice = (cents: number) => {
    return `€${(cents / 100).toFixed(2)}`;
  };

  const formatDate = (dateString: string) => {
    // using en-GB to have DD/MM/YYYY HH:MM
    const date = new Date(dateString);
    return date.toLocaleDateString("en-GB", {
      day: "2-digit",
      month: "short",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "pending":
        return "status-pending";
      case "paid":
        return "status-paid";
      case "cancelled":
        return "status-cancelled";
      default:
        return "";
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case "pending":
        return "Pending";
      case "paid":
        return "Paid";
      case "cancelled":
        return "Cancelled";
      default:
        return status;
    }
  };

  if (loading) {
    return <div className="loading">Loading orders...</div>;
  }

  if (error) {
    return (
      <div className="error-container">
        <div className="error">Error: {error}</div>
        <Link to="/" className="back-link">
          ← Back to catalog
        </Link>
      </div>
    );
  }

  if (orders.length === 0) {
    return (
      <div className="empty-orders">
        <h2>No orders yet</h2>
        <p>
          You haven't placed any orders. Start shopping to see your order history
          here!
        </p>
        <Link to="/" className="btn-back">
          Start Shopping
        </Link>
      </div>
    );
  }

  return (
    <div className="orders-page">
      <h1>Order History</h1>
      <p className="orders-subtitle">View and track your orders</p>

      <div className="orders-list">
        {orders.map((order) => {
          // defensive check in case the backend doesn't include items
          const items = order.items || [];
          const itemCount = items.length;

          return (
            <div key={order.id} className="order-card">
              <div className="order-header">
                <div className="order-id">
                  <span className="order-label">Order #</span>
                  <span className="order-number">{order.id}</span>
                </div>

                <div className="order-date">
                  {formatDate(order.created_at)}
                </div>

                <div
                  className={`order-status ${getStatusColor(order.status)}`}
                >
                  {getStatusText(order.status)}
                </div>
              </div>

              <div className="order-items">
                <h3>Items ({itemCount})</h3>

                {items.map((item) => (
                  <div key={item.id} className="order-item">
                    <div className="order-item-info">
                      <span className="item-quantity">
                        {item.quantity}x {item.product_name}
                      </span>
                      <span className="item-price">
                        {formatPrice(item.unit_price_cents)} each
                      </span>
                    </div>

                    <div className="order-item-total">
                      {formatPrice(
                        item.unit_price_cents * item.quantity
                      )}
                    </div>
                  </div>
                ))}
              </div>

              <div className="order-footer">
                <div className="order-total">
                  <span>Total:</span>
                  <span className="total-amount">
                    {formatPrice(order.total_cents)}
                  </span>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

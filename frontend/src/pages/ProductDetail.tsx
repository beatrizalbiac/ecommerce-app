import { useEffect, useState } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import type { Product } from '../models';
import { getProduct } from '../api/products';
import { useCart } from '../context/cart';
import './ProductDetail.css';

export default function ProductDetail() {
  const { slug } = useParams<{ slug: string }>();
  const navigate = useNavigate();
  const location = useLocation(); // used to return to the exact catalog page
  const { addToCart } = useCart();

  const [product, setProduct] = useState<Product | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [quantity, setQuantity] = useState(1);
  const [addedToCart, setAddedToCart] = useState(false);

  // goes back to the catalog preserving page, filters, etc.
  const handleBackToCatalog = () => {
    const from = location.state?.from;

    if (from) {
      navigate(from, { replace: false });
    } else {
      navigate('/');
    }
  };

  useEffect(() => {
    async function fetchProduct() {
      if (!slug) return;

      setLoading(true);
      setError(null);

      try {
        const data = await getProduct(slug);
        setProduct(data);
      } catch (err) {
        setError(
          err instanceof Error ? err.message : 'Failed to load product'
        );
      } finally {
        setLoading(false);
      }
    }

    fetchProduct();
  }, [slug]);

  const formatPrice = (cents: number) => {
    return `€${(cents / 100).toFixed(2)}`;
  };

  const handleAddToCart = () => {
    if (!product) return;

    // final stock check just in case
    if (quantity > product.stock) {
      alert(`Only ${product.stock} items available`);
      return;
    }

    addToCart(product.id, quantity);
    setAddedToCart(true);

    // simple visual feedback reset
    setTimeout(() => setAddedToCart(false), 2000);
  };

  const handleQuantityChange = (newQuantity: number) => {
    if (!product) return;

    // keeps quantity valid
    if (newQuantity < 1) {
      setQuantity(1);
    } else if (newQuantity > product.stock) {
      setQuantity(product.stock);
    } else {
      setQuantity(newQuantity);
    }
  };

  if (loading) {
    return <div className="loading">Loading product...</div>;
  }

  if (error || !product) {
    return (
      <div className="error-container">
        <div className="error">
          {error || 'Product not found'}
        </div>
        <button
          onClick={handleBackToCatalog}
          className="back-link"
        >
          ← Back to catalog
        </button>
      </div>
    );
  }

  return (
    <div className="product-detail">
      <button
        onClick={handleBackToCatalog}
        className="back-link"
      >
        ← Back to catalog
      </button>

      <div className="product-detail-content">
        <div className="product-image-large">
          <span>📦</span>{/* just to show something, as i'm not going to add actual images for each product */}
        </div>

        <div className="product-detail-info">
          <h1>{product.title}</h1>

          <div className="product-price-large">
            {formatPrice(product.price_cents)}
          </div>

          <div className="product-stock-info">
            {product.stock === 0 ? (
              <span className="out-of-stock">
                Out of stock
              </span>
            ) : product.stock < 5 ? (
              <span className="low-stock">
                Only {product.stock} left in stock
              </span>
            ) : (
              <span className="in-stock">
                In stock
              </span>
            )}
          </div>

          <p className="product-description-full">
            {product.description}
          </p>

          {product.stock > 0 && (
            <div className="add-to-cart-section">
              <div className="quantity-selector">
                <label htmlFor="quantity">Quantity:</label>

                <div className="quantity-controls">
                  <button
                    onClick={() =>
                      handleQuantityChange(quantity - 1)
                    }
                    disabled={quantity <= 1}
                    className="qty-btn"
                  >
                    -
                  </button>

                  <input
                    type="number"
                    id="quantity"
                    value={quantity}
                    onChange={(e) =>
                      handleQuantityChange(
                        parseInt(e.target.value) || 1
                      )
                    }
                    min="1"
                    max={product.stock}
                    className="qty-input"
                  />

                  <button
                    onClick={() =>
                      handleQuantityChange(quantity + 1)
                    }
                    disabled={quantity >= product.stock}
                    className="qty-btn"
                  >
                    +
                  </button>
                </div>
              </div>

              <button
                onClick={handleAddToCart}
                className={`add-to-cart-btn ${
                  addedToCart ? 'added' : ''
                }`}
                disabled={addedToCart}
              >
                {addedToCart
                  ? 'Added to cart!'
                  : 'Add to cart'}
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

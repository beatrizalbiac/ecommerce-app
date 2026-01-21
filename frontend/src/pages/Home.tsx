import { useEffect, useRef, useState } from "react";
import { Link, useLocation, useSearchParams } from "react-router-dom";
import type { Product } from "../models";
import { getProducts } from "../api/products";
import "./Home.css";

const SHOWN = 9; // same limit as in the backend

export default function Home() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [searchInput, setSearchInput] = useState("");
  const [searchQuery, setSearchQuery] = useState("");
  const [sortBy, setSortBy] =
    useState<"price_asc" | "price_desc" | "newest" | "">("");

  const [searchParams, setSearchParams] = useSearchParams();
  const location = useLocation(); // only used to remember where we came from
  const [hasNext, setHasNext] = useState(false); // enables / disables next page button

  // page always comes from the URL, not from local state
  const pageFromUrl = Number(searchParams.get("page") ?? "1");
  const page =
    Number.isFinite(pageFromUrl) && pageFromUrl >= 1 ? pageFromUrl : 1;

  const changePage = (newPage: number) => {
    const next = new URLSearchParams(searchParams);
    next.set("page", String(newPage)); // keeps the rest of the params untouched
    setSearchParams(next);
  };

  const prevSearchQuery = useRef(searchQuery);
  const prevSortBy = useRef(sortBy);

  useEffect(() => {
    const searchChanged = prevSearchQuery.current !== searchQuery;
    const sortChanged = prevSortBy.current !== sortBy;

    // only resets the page if search or sort actually changed
    if (searchChanged || sortChanged) {
      changePage(1);
    }

    prevSearchQuery.current = searchQuery;
    prevSortBy.current = sortBy;
  }, [searchQuery, sortBy]);

  useEffect(() => {
    async function fetchProducts() {
      setLoading(true);
      setError(null);

      try {
        const data = await getProducts({
          q: searchQuery || undefined, // avoids sending an empty query
          sort: sortBy || undefined,
          page,
          shown: SHOWN,
        });

        setProducts(data);
        setHasNext(data.length === SHOWN);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load products");
      } finally {
        setLoading(false);
      }
    }

    fetchProducts();
  }, [searchQuery, sortBy, page]);

  const formatPrice = (cents: number) =>
    `€${(cents / 100).toFixed(2)}`;

  if (loading) return <div className="loading">Loading products...</div>;
  if (error) return <div className="error">Error: {error}</div>;

  // saved so ProductDetail can send us back to the same page w the filters
  const from = location.pathname + location.search;

  return (
    <div className="home">
      <div className="home-header">
        <h1>Product Catalog</h1>

        <div className="filters">
          <input
            type="search"
            placeholder="Search products..."
            value={searchInput}
            onChange={(e) => setSearchInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                setSearchQuery(searchInput.trim()); // search only happens on enter
              }
            }}
            className="search-input"
          />

          <select
            value={sortBy}
            onChange={(e) =>
              setSortBy(e.target.value as any) // select values are always strings
            }
            className="sort-select"
          >
            <option value="">Sort by...</option>
            <option value="price_asc">Price: Low to High</option>
            <option value="price_desc">Price: High to Low</option>
            <option value="newest">Newest First</option>
          </select>
        </div>
      </div>

      {products.length === 0 ? (
        <p className="no-products">No products found</p>
      ) : (
        <>
          <div className="products-grid">
            {products.map((product) => (
              <Link
                key={product.id}
                to={`/products/${product.slug}`}
                state={{ from }} // so we can come back here
                className="product-card"
              >
                <div className="product-image-placeholder">
                  <span>📦</span>
                </div>

                <div className="product-info">
                  <h3>{product.title}</h3>

                  <p className="product-description">
                    {product.description.substring(0, 100)}
                    {product.description.length > 100 ? "..." : ""}
                  </p>

                  <div className="product-footer">
                    <span className="product-price">
                      {formatPrice(product.price_cents)}
                    </span>

                    <span className="product-stock">
                      {product.stock === 0 ? (
                        <span className="out-of-stock">
                          Out of stock
                        </span>
                      ) : product.stock < 5 ? (
                        <span className="low-stock">
                          Only {product.stock} left
                        </span>
                      ) : null}
                    </span>
                  </div>
                </div>
              </Link>
            ))}
          </div>

          <div className="pager">
            <button
              className="pager-btn"
              onClick={() =>
                changePage(Math.max(1, page - 1))
              }
              disabled={page === 1}
              aria-label="Previous page"
            >
              ‹
            </button>

            <div className="pager-label">
              Page {page}
            </div>

            <button
              className="pager-btn"
              onClick={() => changePage(page + 1)}
              disabled={!hasNext}
              aria-label="Next page"
            >
              ›
            </button>
          </div>
        </>
      )}
    </div>
  );
}

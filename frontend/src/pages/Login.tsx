import { useState } from "react";
import type { FormEvent } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../context/auth";
import "./Auth.css";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError(null); // reset previous error before attempting login
    setLoading(true);

    try {
      await login(email, password); // backend handles credential validation
      navigate("/"); // redirect after successful login
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to login");
    } finally {
      setLoading(false); // make sure loading state is always reset
    }
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <h1>Login</h1>
        <p className="subtitle">Welcome back💚</p>

        {error && <div className="error-message">{error}</div>}

        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              placeholder="your@email.com"
              disabled={loading} // prevent edits while request is in progress
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              placeholder="••••••••"
              disabled={loading}
            />
          </div>

          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? "Logging in..." : "Login"}
          </button>
        </form>

        <p className="register-link">
          Don't have an account? <Link to="/register">Register here</Link>
        </p>
      </div>
    </div>
  );
}

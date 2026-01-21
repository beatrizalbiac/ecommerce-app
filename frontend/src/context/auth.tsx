import { createContext, useContext, useState, useEffect } from "react";
import type { ReactNode } from "react";
import type { User, RegisterRequest } from "../models";
import { login as apiLogin, register as apiRegister, getCurrentUser } from "../api/auth";

interface AuthContextType {
  user: User | null;
  token: string | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (data: RegisterRequest) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const savedToken = localStorage.getItem("token");
    if (savedToken) {
      setToken(savedToken); // keep token in state so the app knows the user might be logged in

      getCurrentUser(savedToken)
        .then(setUser) // token is valid, so we can safely load the user
        .catch(() => {
          // if the token is invalid / expired, clean everything and start fresh
          localStorage.removeItem("token");
          setToken(null);
        })
        .finally(() => setLoading(false)); // auth check finished, app can render normally
    } else {
      setLoading(false); // no token at all, so we already know the user is logged out
    }
  }, []);

  const login = async (email: string, password: string) => {
    const authResponse = await apiLogin(email, password);
    const newToken = authResponse.access_token;

    setToken(newToken);
    localStorage.setItem("token", newToken); // persist session so it survives page reloads

    const userInfo = await getCurrentUser(newToken); // fetch full user info using the new token
    setUser(userInfo);
  };

  const register = async (data: RegisterRequest) => {
    await apiRegister(data); // backend already validates everything
    await login(data.email, data.password); // auto-login after successful registration
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem("token"); // remove token so the session is fully cleared
  };

  return (
    <AuthContext.Provider value={{ user, token, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
}

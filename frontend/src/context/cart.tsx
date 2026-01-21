import { createContext, useContext, useState, useEffect } from "react";
import type { ReactNode } from "react";
import type { CartItem } from "../models";

interface CartContextType {
  cart: CartItem[];
  addToCart: (productId: number, quantity: number) => void;
  removeFromCart: (productId: number) => void;
  updateQuantity: (productId: number, quantity: number) => void;
  clearCart: () => void;
  getCartTotal: () => number;
}

const CartContext = createContext<CartContextType | undefined>(undefined);

export function CartProvider({ children }: { children: ReactNode }) {
  const [cart, setCart] = useState<CartItem[]>(() => {
    const savedCart = localStorage.getItem("cart");
    if (savedCart) {
      try {
        return JSON.parse(savedCart); // cart is stored as plain JSON, so it needs to be parsed on init
      } catch {
        return []; // if localStorage is corrupted, just start with an empty cart
      }
    }
    return [];
  });

  useEffect(() => {
    localStorage.setItem("cart", JSON.stringify(cart)); // keep cart in sync so it survives page reloads
  }, [cart]);

  const addToCart = (productId: number, quantity: number) => {
    setCart((prevCart) => {
      const existingItem = prevCart.find(
        (item) => item.product_id === productId
      );

      if (existingItem) {
        return prevCart.map((item) =>
          item.product_id === productId
            ? { ...item, quantity: item.quantity + quantity } // merge quantities instead of duplicating entries
            : item
        );
      }

      return [...prevCart, { product_id: productId, quantity }]; // only minimal data is stored in the cart
    });
  };

  const removeFromCart = (productId: number) => {
    setCart((prevCart) =>
      prevCart.filter((item) => item.product_id !== productId)
    );
  };

  const updateQuantity = (productId: number, quantity: number) => {
    if (quantity <= 0) {
      removeFromCart(productId); // if the quantity is equal to or below 0 it's treated as removing the item
      return;
    }

    setCart((prevCart) =>
      prevCart.map((item) =>
        item.product_id === productId ? { ...item, quantity } : item
      )
    );
  };

  const clearCart = () => {
    setCart([]); // reset cart state
    localStorage.removeItem("cart"); // explicitly clear storage instead of keeping an empty array
  };

  const getCartTotal = () => {
    return cart.reduce(
      (total, item) => total + item.quantity,
      0
    ); // returns the total number of items
  };

  return (
    <CartContext.Provider
      value={{
        cart,
        addToCart,
        removeFromCart,
        updateQuantity,
        clearCart,
        getCartTotal,
      }}
    >
      {children}
    </CartContext.Provider>
  );
}

export function useCart() {
  const context = useContext(CartContext);
  if (context === undefined) {
    throw new Error("useCart must be used within CartProvider");
  }
  return context;
}

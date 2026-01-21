import type { CartItem, CartValidationResponse } from "../models";

const API_BASE_URL = import.meta.env.VITE_API_URL;

// validated here before creating the order (backend validates it again anyway)
export async function validateCart(items: CartItem[]): Promise<CartValidationResponse> { // Promise is there bc the function is async in the backend so it isn't instantly returned
  const response = await fetch(`${API_BASE_URL}/checkout/validate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ items }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail);
  }

  return response.json();
}
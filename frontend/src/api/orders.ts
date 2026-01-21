import type { Order, CartItem } from "../models";

const API_BASE_URL = import.meta.env.VITE_API_URL;

// it always checks the authentication of the user before modifying their data.

export async function createOrder(items: CartItem[], token: string): Promise<Order> {
  const response = await fetch(`${API_BASE_URL}/orders`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ items }),
  });

  if (!response.ok) {
    const error = await response.json();
    if (response.status === 401) {
      throw new Error("You must be logged in to view orders");
    }
    throw new Error(error.detail);
  }

  return response.json();
}

// gets ALL orders for the user
export async function getUserOrders(token: string): Promise<Order[]> {
  const response = await fetch(`${API_BASE_URL}/orders`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    const error = await response.json();
    if (response.status === 401) {
      throw new Error("You must be logged in to view orders");
    }
    throw new Error(error.detail);
  }

  return response.json();
}

// gets just one order
export async function getOrder(orderId: number, token: string): Promise<Order> {
  const response = await fetch(`${API_BASE_URL}/orders/${orderId}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    if (response.status === 401) {
      throw new Error("Unauthorized");
    }
    if (response.status === 404) {
      throw new Error("Order not found");
    }
    throw new Error("Failed to fetch order");
  }

  return response.json();
}
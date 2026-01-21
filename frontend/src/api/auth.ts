import type { User, LoginRequest, RegisterRequest, AuthResponse } from "../models";

const API_BASE_URL = import.meta.env.VITE_API_URL;

export async function register(data: RegisterRequest): Promise<User> {
  const response = await fetch(`${API_BASE_URL}/auth/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const error = await response.json();
    if (response.status === 409) {
      throw new Error(error.detail); // it takes the msg defined in the backend and reuses it
    }
    throw new Error("Failed to register");
  }

  return response.json();
}

export async function login(email: string, password: string): Promise<AuthResponse> {
  // backend expects FormData format for OAuth2
  const formData = new URLSearchParams();
  formData.append("username", email); // as said in the backend the "username" is instead the email
  formData.append("password", password);

  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json();
    if (response.status === 401) {
      throw new Error(error.detail);
    }
    throw new Error("Failed to login");
  }

  return response.json();
}

export async function getCurrentUser(token: string): Promise<User> {
  const response = await fetch(`${API_BASE_URL}/auth/me`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    if (response.status === 401) {
      throw new Error("Unauthorized");
    }
    throw new Error("Failed to get user info");
  }

  return response.json();
}
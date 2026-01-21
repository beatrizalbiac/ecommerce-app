export interface User {
  id: number;
  name: string;
  lastname: string;
  email: string;
  is_admin: boolean;
  created_at: string;
}

export interface LoginRequest {
  username: string; // it's refered to as username but in reality is the email
  password: string;
}

export interface RegisterRequest {
  name: string;
  lastname: string;
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface Product {
  id: number;
  title: string;
  slug: string;
  description: string;
  price_cents: number;
  currency: string;
  stock: number;
  created_at: string;
  updated_at: string;
}

export interface OrderItem {
  id: number;
  order_id: number;
  product_id: number;
  product_name: string; 
  unit_price_cents: number; // it stores the name and price at the time of purchase, so it the price changes after it still shows what was actually paid
  quantity: number;
}

export interface Order {
  id: number;
  user_id: number;
  status: "pending" | "paid" | "cancelled";
  total_cents: number;
  currency: string;
  created_at: string;
  items: OrderItem[];
}

export interface OrderCreateRequest {
  items: CartItem[];
}

export interface CartItem {
  product_id: number;
  quantity: number;
}

export interface CartItemWithDetails extends CartItem {
  product: Product; // frontend only
}

export interface CartItemValidated {
  product_id: number;
  title: string;
  slug: string;
  price_cents: number;
  quantity: number;
  total_price: number;
  available_stock: number;
  available: boolean;
}

export interface CartValidationResponse {
  items: CartItemValidated[];
  total_cents: number;
  currency: string;
  all_available: boolean;
}
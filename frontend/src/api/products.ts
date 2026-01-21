import type { Product } from "../models";

const API_BASE_URL = import.meta.env.VITE_API_URL;

export interface ProductsParams {
  q?: string;
  page?: number;
  shown?: number;
  sort?: "price_asc" | "price_desc" | "newest";
}

/**
 * Get all products with optional filters
 */
export async function getProducts(params: ProductsParams = {}): Promise<Product[]> {
  const { q, page = 1, shown = 9, sort } = params; // it's also defined in the backend, but js in case I defined them here too
  
  const searchParams = new URLSearchParams();
  if (q) searchParams.append("q", q); // so it only gets sent if it exists
  searchParams.append("page", page.toString());
  searchParams.append("shown", shown.toString());
  if (sort) searchParams.append("sort", sort);

  const response = await fetch(`${API_BASE_URL}/products?${searchParams}`);
  
  if (!response.ok) {
    throw new Error("Failed to fetch products");
  }

  return response.json();
}

// get a product using the slug
export async function getProduct(slug: string): Promise<Product> {
  const response = await fetch(`${API_BASE_URL}/products/slug/${slug}`); // there's an extra "slug" in the link parts so it doesn't read a slug as an id or viceversa
  
  if (!response.ok) {
    if (response.status === 404) {
      throw new Error("Product not found");
    }
    throw new Error("Failed to fetch product");
  }

  return response.json();
}

// get a product using the id
export async function getProductById(id: number): Promise<Product> {
  const response = await fetch(`${API_BASE_URL}/products/${id}`);

  if (!response.ok) {
    if (response.status === 404) {
      throw new Error("Product not found");
    }
    throw new Error("Failed to fetch product");
  }

  return response.json();
}
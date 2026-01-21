# Full-Stack E-Commerce Application → BAECOMMERCE
*By Beatriz Albiac*

## URLs
**web:** https://baecommerce.vercel.app  
**backend:** https://baecommerce.onrender.com/docs

## Overview
In this project a small e-commerce web application was created. The web theme goes around tech products such as phones, laptops, mouses etc.
The web allows users to browse products, manage their cart, place orders, create an account and log into it, as well as seeing their past order history.

To add all these functionalityes the project was split into two:
- **Backend:** Build with FastAPI and SQLModel, deploying the database into Supabase  
- **Frontend:** A single page application built with React and TypeScript

## Project structure
```bash
ecommerce-app/
├── backend/
│   ├── app/
│   │   ├── main.py          
│   │   ├── db.py            
│   │   ├── auth.py          # To help with the authentication process
│   │   ├── dependencies.py  # Shared FastAPI dependencies
│   │   ├── models/          # Data models (User, Product, Order, OrderItem)
│   │   ├── servuces/        # To separate some functionalities
│   │   └── routers/         # API endpoints (auth, products, checkout, orders)
│   └── requirements.txt 
│
└── frontend/
    ├── src/
    │   ├── api/             # Functions for communicating with the backend API
    │   ├── assets/          
    │   ├── components/      # The main Layout
    │   ├── context/         # Global state management
    │   ├── models/          # Frontend data types / interfaces
    │   ├── pages/           # Application views (catalog, product detail, cart, auth, orders)
    │   ├── index.css        # Global styles
    │   ├── main.tsx         # React entry point
    │   └── routes.tsx       # Client-side routing configuration
    └── package.json        
        └── routes.tsx       # Client-side routing configuration
```

## Data models
The application uses mainly the data models defined in the assignment. These being User, Product, Order and OrderItem.
Product has been pre-poblated so there are products to browse from the start.

**Minor implementation changes:**
- Although the Cart is part of the data model, it is handled on the client side and checked by the server during checkout, instead of being stored in the database.
- OrderItem stores the unit price at the moment of purchase and does not update that value even if the price of the product is updated. This is to keep everything consistent, and to actually show what was paid in the moment.

On the frontend, React Context is used to manage global state such as authentication and the shopping cart, avoiding prop drilling and keeping the state centralized.

## API structure
These are the main endpoints (functionalities) that the app has:
- **health:** Just to chek if it works.
- **products:** Product catalog and product details.
- **auth:** User registration, login and authentication.
- **orders:** Order creation and order history.
- **checkout:** Cart validation (before creating a order).

Admin users and endpoints were not integrated because of time issues. This means that intuitive endpoints, such as product and users management (erasing, creating etc.), were not implemented. However, the database is set up so there could exist admins in a future upgrade.

## Frontend views
- **Product catalog:** Displays a list of products, you can search, filter and browse different pages.
- **Product detail:** Shows the detailed information on a specific product, and allows it to be added into the cart (and to change the amount).
- **Cart:** Displays the current products that a user has added into the cart. It allows quantity changes and item removal showing the complete price of the cart added up.
- **Checkout:** Validates the cart and allows the order confirmation only if the user is logged in. Here is where the payment would happen in a real life-scenario, but that functionality was not added here.
- **Orders** Displays a history of a users orders and what was ordered when. It shows them in order from the newest to the oldest order.
- **Login/Register:** Allows users to create an account or to get into their account.

## Logic
- The shopping cart is managed on the client side for responsiveness.
- Before creating an order, the cart is validated by the backend to ensure:
  - Product availability
  - Correct prices
  - Sufficient stock
- Stock is reduced when an order is successfully created. In the future a "holding" system could be implemented, so while a product is on someone's cart the product is reserved in some way.
- Only authenticated users can place orders and access their order history.

## To run the project locally
**Backend**
```bash
cd backend
pip install -r requirements.txt
fastapi dev
```
The backend will be available at http://localhost:8000

**Frontend**
```bash
yarn install
yarn dev
```
The frontend will be available at http://localhost:5173

## Extras
No additional features beyond the requirements were implemented.  

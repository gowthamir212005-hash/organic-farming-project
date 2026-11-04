# Organic Farming — Database Schema & ER Diagram

Project: Organic Farming E‑Commerce Management System

Palette (use in reports/slides):
- Project Title: Dark Forest Green (#1B5E20)
- Table Headers: Organic Green (#2E7D32)
- Header Text: White (#FFFFFF)
- Primary Keys (PK): Soft Gold (#FFD54F)
- Foreign Keys (FK): Light Green (#C8E6C9)
- Table Background: Very Light Green (#F1F8E9)
- Borders: Gray-Green (#A5D6A7)
- Text: Dark Gray (#263238)

---

## Overview
This document defines a professional, normalized relational schema for the Organic Farming e‑commerce system and provides a visual ER diagram (Mermaid) styled to the requested agriculture theme. The design is normalized for clarity and reporting and suitable for an MCA final-year project report and viva.

Design goals:
- Clear PK/FK relationships
- Auditable created/updated timestamps
- Support for carts, itemized orders, payments, delivery and feedback
- Admin table for site operators

---

## Tables (concise definitions)

All `id` fields are integer primary keys (auto-increment). Timestamps use `DATETIME` / `TIMESTAMP`.

1) Customer
- `id` PK
- `name` VARCHAR(150) NOT NULL
- `email` VARCHAR(254) UNIQUE NOT NULL
- `phone` VARCHAR(20) NOT NULL
- `address` TEXT
- `city` VARCHAR(100)
- `pincode` VARCHAR(12)
- `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
- `updated_at` DATETIME

2) Category
- `id` PK
- `name` VARCHAR(100) NOT NULL
- `slug` VARCHAR(120) UNIQUE
- `description` TEXT
- `parent_id` FK -> Category(id) NULL (for category hierarchy)
- `created_at`, `updated_at`

3) Product
- `id` PK
- `category_id` FK -> Category(id)
- `name` VARCHAR(200) NOT NULL
- `sku` VARCHAR(64) UNIQUE
- `description` TEXT
- `price` DECIMAL(10,2) NOT NULL
- `stock` INT DEFAULT 0
- `image` VARCHAR(300)
- `created_at`, `updated_at`

4) Cart
- `id` PK
- `customer_id` FK -> Customer(id)
- `created_at`, `updated_at`
- Note: cart contents are stored in `cart_items` table to normalize

5) CartItem
- `id` PK
- `cart_id` FK -> Cart(id)
- `product_id` FK -> Product(id)
- `quantity` INT NOT NULL DEFAULT 1
- `unit_price` DECIMAL(10,2) NOT NULL
- unique(cart_id, product_id)

6) Order
- `id` PK
- `customer_id` FK -> Customer(id)
- `order_number` VARCHAR(40) UNIQUE NOT NULL
- `total_amount` DECIMAL(10,2) NOT NULL
- `status` VARCHAR(30) NOT NULL DEFAULT 'pending'  -- (pending, confirmed, shipped, delivered, cancelled)
- `payment_id` FK -> Payment(id) NULL
- `delivery_id` FK -> Delivery(id) NULL
- `created_at`, `updated_at`

7) OrderItem
- `id` PK
- `order_id` FK -> Order(id)
- `product_id` FK -> Product(id)
- `quantity` INT NOT NULL
- `unit_price` DECIMAL(10,2) NOT NULL
- `subtotal` DECIMAL(10,2) NOT NULL -- computed: quantity * unit_price

8) Payment
- `id` PK
- `order_id` FK -> Order(id) UNIQUE (one-to-one)
- `method` VARCHAR(30) NOT NULL -- (cod, gpay, phonepay, card, wallet)
- `amount` DECIMAL(10,2) NOT NULL
- `status` VARCHAR(30) NOT NULL DEFAULT 'pending' -- (pending, paid, failed, refunded)
- `transaction_ref` VARCHAR(200)
- `paid_at` DATETIME NULL
- `created_at`, `updated_at`

9) Delivery
- `id` PK
- `order_id` FK -> Order(id) UNIQUE
- `recipient_name` VARCHAR(150)
- `phone` VARCHAR(20)
- `address` TEXT
- `city` VARCHAR(100)
- `pincode` VARCHAR(12)
- `delivery_status` VARCHAR(30) DEFAULT 'pending' -- (pending, shipped, out_for_delivery, delivered, returned)
- `tracking_number` VARCHAR(120)
- `shipped_at` DATETIME NULL
- `delivered_at` DATETIME NULL
- `created_at`, `updated_at`

10) Admin
- `id` PK
- `username` VARCHAR(150) UNIQUE
- `full_name` VARCHAR(150)
- `email` VARCHAR(254) UNIQUE
- `role` VARCHAR(50) -- (superadmin, manager, support)
- `phone` VARCHAR(20)
- `created_at`, `updated_at`

11) Feedback
- `id` PK
- `customer_id` FK -> Customer(id)
- `product_id` FK -> Product(id) NULL
- `order_id` FK -> Order(id) NULL
- `rating` INT CHECK (rating BETWEEN 1 AND 5)
- `comment` TEXT
- `created_at` DATETIME

---

## Referential integrity & indexes (high-level)
- FK constraints between Product.category_id → Category.id
- FK constraints between Order.customer_id → Customer.id
- FK constraints between OrderItem.order_id → Order.id, OrderItem.product_id → Product.id
- Unique indexes on `email` (Customer), `sku` (Product), `order_number` (Order)
- Composite index on CartItem(cart_id, product_id)
- Use ON DELETE CASCADE for OrderItems when Order deleted; use ON DELETE SET NULL for Payment, Delivery references if necessary.

---

## Example SQL DDL (concise, compatible with MySQL/Postgres)

```sql
CREATE TABLE customer (
  id SERIAL PRIMARY KEY,
  name VARCHAR(150) NOT NULL,
  email VARCHAR(254) NOT NULL UNIQUE,
  phone VARCHAR(20) NOT NULL,
  address TEXT,
  city VARCHAR(100),
  pincode VARCHAR(12),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP
);

CREATE TABLE category (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  slug VARCHAR(120) UNIQUE,
  description TEXT,
  parent_id INT REFERENCES category(id) ON DELETE SET NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP
);

CREATE TABLE product (
  id SERIAL PRIMARY KEY,
  category_id INT REFERENCES category(id) ON DELETE SET NULL,
  name VARCHAR(200) NOT NULL,
  sku VARCHAR(64) UNIQUE,
  description TEXT,
  price DECIMAL(10,2) NOT NULL,
  stock INT DEFAULT 0,
  image VARCHAR(300),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP
);

CREATE TABLE cart (
  id SERIAL PRIMARY KEY,
  customer_id INT REFERENCES customer(id) ON DELETE CASCADE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP
);

CREATE TABLE cart_item (
  id SERIAL PRIMARY KEY,
  cart_id INT REFERENCES cart(id) ON DELETE CASCADE,
  product_id INT REFERENCES product(id) ON DELETE RESTRICT,
  quantity INT NOT NULL DEFAULT 1,
  unit_price DECIMAL(10,2) NOT NULL,
  UNIQUE(cart_id, product_id)
);

CREATE TABLE "order" (
  id SERIAL PRIMARY KEY,
  customer_id INT REFERENCES customer(id) ON DELETE SET NULL,
  order_number VARCHAR(40) UNIQUE NOT NULL,
  total_amount DECIMAL(10,2) NOT NULL,
  status VARCHAR(30) NOT NULL DEFAULT 'pending',
  payment_id INT,
  delivery_id INT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP
);

CREATE TABLE order_item (
  id SERIAL PRIMARY KEY,
  order_id INT REFERENCES "order"(id) ON DELETE CASCADE,
  product_id INT REFERENCES product(id) ON DELETE RESTRICT,
  quantity INT NOT NULL,
  unit_price DECIMAL(10,2) NOT NULL,
  subtotal DECIMAL(10,2) NOT NULL
);

CREATE TABLE payment (
  id SERIAL PRIMARY KEY,
  order_id INT REFERENCES "order"(id) ON DELETE CASCADE,
  method VARCHAR(30) NOT NULL,
  amount DECIMAL(10,2) NOT NULL,
  status VARCHAR(30) NOT NULL DEFAULT 'pending',
  transaction_ref VARCHAR(200),
  paid_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP
);

CREATE TABLE delivery (
  id SERIAL PRIMARY KEY,
  order_id INT REFERENCES "order"(id) ON DELETE CASCADE,
  recipient_name VARCHAR(150),
  phone VARCHAR(20),
  address TEXT,
  city VARCHAR(100),
  pincode VARCHAR(12),
  delivery_status VARCHAR(30) DEFAULT 'pending',
  tracking_number VARCHAR(120),
  shipped_at TIMESTAMP,
  delivered_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP
);

CREATE TABLE admin (
  id SERIAL PRIMARY KEY,
  username VARCHAR(150) UNIQUE,
  full_name VARCHAR(150),
  email VARCHAR(254) UNIQUE,
  role VARCHAR(50),
  phone VARCHAR(20),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP
);

CREATE TABLE feedback (
  id SERIAL PRIMARY KEY,
  customer_id INT REFERENCES customer(id) ON DELETE CASCADE,
  product_id INT REFERENCES product(id) ON DELETE SET NULL,
  order_id INT REFERENCES "order"(id) ON DELETE SET NULL,
  rating INT CHECK (rating >= 1 AND rating <= 5),
  comment TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Mermaid ER Diagram (copy into Markdown that supports Mermaid or into mermaid.live)

```mermaid
flowchart LR
  %% Title area is not a node, use text above the diagram when rendering

  subgraph CustomerTable[Customer]
    direction TB
    C_ID[(PK id)]
    C_NAME[name]
    C_EMAIL[email]
    C_PHONE[phone]
  end
  style CustomerTable fill:#F1F8E9,stroke:#A5D6A7,color:#263238
  style C_ID fill:#FFD54F,stroke:#A5D6A7,color:#263238
  style C_NAME fill:#FFFFFF,stroke:#A5D6A7,color:#263238
  style C_EMAIL fill:#FFFFFF,stroke:#A5D6A7,color:#263238
  style C_PHONE fill:#FFFFFF,stroke:#A5D6A7,color:#263238

  subgraph CategoryTable[Category]
    direction TB
    CAT_ID[(PK id)]
    CAT_NAME[name]
    CAT_PARENT[(FK parent_id)]
  end
  style CategoryTable fill:#F1F8E9,stroke:#A5D6A7,color:#263238
  style CAT_ID fill:#FFD54F,stroke:#A5D6A7,color:#263238
  style CAT_NAME fill:#FFFFFF,stroke:#A5D6A7,color:#263238
  style CAT_PARENT fill:#C8E6C9,stroke:#A5D6A7,color:#263238

  subgraph ProductTable[Product]
    direction TB
    P_ID[(PK id)]
    P_CAT[(FK category_id)]
    P_NAME[name]
    P_PRICE[price]
  end
  style ProductTable fill:#F1F8E9,stroke:#A5D6A7,color:#263238
  style P_ID fill:#FFD54F,stroke:#A5D6A7,color:#263238
  style P_CAT fill:#C8E6C9,stroke:#A5D6A7,color:#263238
  style P_NAME fill:#FFFFFF,stroke:#A5D6A7,color:#263238
  style P_PRICE fill:#FFFFFF,stroke:#A5D6A7,color:#263238

  subgraph CartTable[Cart]
    direction TB
    CART_ID[(PK id)]
    CART_CUST[(FK customer_id)]
  end
  style CartTable fill:#F1F8E9,stroke:#A5D6A7,color:#263238
  style CART_ID fill:#FFD54F,stroke:#A5D6A7,color:#263238
  style CART_CUST fill:#C8E6C9,stroke:#A5D6A7,color:#263238

  subgraph CartItemTable[CartItem]
    direction TB
    CI_ID[(PK id)]
    CI_CART[(FK cart_id)]
    CI_PRODUCT[(FK product_id)]
    CI_QTY[quantity]
  end
  style CartItemTable fill:#F1F8E9,stroke:#A5D6A7,color:#263238
  style CI_ID fill:#FFD54F,stroke:#A5D6A7,color:#263238
  style CI_CART fill:#C8E6C9,stroke:#A5D6A7,color:#263238
  style CI_PRODUCT fill:#C8E6C9,stroke:#A5D6A7,color:#263238
  style CI_QTY fill:#FFFFFF,stroke:#A5D6A7,color:#263238

  subgraph OrderTable[Order]
    direction TB
    O_ID[(PK id)]
    O_CUST[(FK customer_id)]
    O_NUM[order_number]
    O_TOTAL[total_amount]
  end
  style OrderTable fill:#F1F8E9,stroke:#A5D6A7,color:#263238
  style O_ID fill:#FFD54F,stroke:#A5D6A7,color:#263238
  style O_CUST fill:#C8E6C9,stroke:#A5D6A7,color:#263238
  style O_NUM fill:#FFFFFF,stroke:#A5D6A7,color:#263238
  style O_TOTAL fill:#FFFFFF,stroke:#A5D6A7,color:#263238

  subgraph OrderItemTable[OrderItem]
    direction TB
    OI_ID[(PK id)]
    OI_ORDER[(FK order_id)]
    OI_PRODUCT[(FK product_id)]
    OI_QTY[quantity]
  end
  style OrderItemTable fill:#F1F8E9,stroke:#A5D6A7,color:#263238
  style OI_ID fill:#FFD54F,stroke:#A5D6A7,color:#263238
  style OI_ORDER fill:#C8E6C9,stroke:#A5D6A7,color:#263238
  style OI_PRODUCT fill:#C8E6C9,stroke:#A5D6A7,color:#263238
  style OI_QTY fill:#FFFFFF,stroke:#A5D6A7,color:#263238

  subgraph PaymentTable[Payment]
    direction TB
    PAY_ID[(PK id)]
    PAY_ORDER[(FK order_id)]
    PAY_METHOD[method]
    PAY_AMOUNT[amount]
  end
  style PaymentTable fill:#F1F8E9,stroke:#A5D6A7
  style PAY_ID fill:#FFD54F
  style PAY_ORDER fill:#C8E6C9

  subgraph DeliveryTable[Delivery]
    direction TB
    D_ID[(PK id)]
    D_ORDER[(FK order_id)]
    D_STATUS[delivery_status]
  end
  style DeliveryTable fill:#F1F8E9,stroke:#A5D6A7
  style D_ID fill:#FFD54F
  style D_ORDER fill:#C8E6C9

  subgraph AdminTable[Admin]
    direction TB
    A_ID[(PK id)]
    A_USER[username]
    A_ROLE[role]
  end
  style AdminTable fill:#F1F8E9,stroke:#A5D6A7
  style A_ID fill:#FFD54F

  subgraph FeedbackTable[Feedback]
    direction TB
    F_ID[(PK id)]
    F_CUST[(FK customer_id)]
    F_PRODUCT[(FK product_id)]
    F_RATING[rating]
  end
  style FeedbackTable fill:#F1F8E9,stroke:#A5D6A7
  style F_ID fill:#FFD54F
  style F_CUST fill:#C8E6C9
  style F_PRODUCT fill:#C8E6C9

  %% Relationships
  C_ID -->|places| OrderTable
  OrderTable -->|has| OrderItemTable
  ProductTable -->|included in| OrderItemTable
  CategoryTable -->|categorizes| ProductTable
  CustomerTable -->|owns| CartTable
  CartTable -->|contains| CartItemTable
  ProductTable -->|in cart| CartItemTable
  OrderTable -->|paid via| PaymentTable
  OrderTable -->|delivered by| DeliveryTable
  CustomerTable -->|gives| FeedbackTable
  ProductTable -->|receives| FeedbackTable

``` 

---

## How to use
- Paste the Mermaid block into a Markdown viewer that supports Mermaid (GitHub does not render Mermaid by default) or use https://mermaid.live to get a high-resolution PNG/SVG for your report.
- Use the SQL DDL to create your schema in Postgres or MySQL. Adjust `SERIAL` vs `AUTO_INCREMENT` for engine.

---

## Next steps (suggested)
- Export mermaid diagram into SVG/PNG for your report
- Prepare an ER diagram image and include in the viva slides
- Optionally add audit fields (`created_by`, `updated_by`) and soft-delete flags (`is_active`) if required


*File generated by assistant — edit as needed for final report.*

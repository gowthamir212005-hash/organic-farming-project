# Organic Farm Database Design

This document describes the Organic Farm database architecture with a personalized, organic-commerce approach.
It is written to match your project’s frontend styling, Django admin workflow, and the business needs of an organic grocery store.

## Core Models

### Category
- `name` (unique)
- `slug` (unique)
- `description`
- `is_active`
- `created_at`, `updated_at`

Used to group produce categories such as Fruit, Dairy, Dry Fruits, Vegetables, etc.

### Product
- `category` → `Category`
- `sku` (unique)
- `name`
- `slug`
- `description`
- `price`
- `inventory`
- `unit`
- `image`
- `is_organic`
- `is_active`
- `created_at`, `updated_at`

This supports catalog management, inventory tracking, and product metadata.

### CustomerProfile
- `user` → Django `User`
- `phone`
- `created_at`, `updated_at`

Stores extra profile data for logged-in users.

### Address
- `user` → Django `User`
- `label`
- `full_name`
- `phone`
- `address_line`
- `city`
- `pincode`
- `is_default`
- `created_at`, `updated_at`

Allows multiple shipping addresses per customer.

### Cart
- `user` → Django `User`
- `is_active`
- `created_at`, `updated_at`

Stores the active cart for a user. Can be extended to support guest carts later.

### CartItem
- `cart` → `Cart`
- `product` → `Product`
- `quantity`
- `unit_price`
- `created_at`, `updated_at`

Keeps cart items normalized and ready for checkout.

### Order
- `user` → Django `User`
- `shipping_address` → `Address`
- `name`, `phone`, `address`, `city`, `pincode`
- `payment_method`
- `status`
- `subtotal`
- `shipping_fee`
- `discount`
- `total_amount`
- `created_at`, `updated_at`

Supports order lifecycle tracking, payment method selection, and total calculation.

### OrderItem
- `order` → `Order`
- `product` → `Product`
- `quantity`
- `unit_price`
- `total_price`
- `created_at`, `updated_at`

Tracks the exact items purchased by order.

### PaymentTransaction
- `order` → `Order`
- `transaction_id`
- `provider`
- `amount`
- `status`
- `metadata`
- `created_at`, `updated_at`

Captures payment gateway transaction details and statuses.

## Integration Notes

- The new models are implemented in `farming/models.py`.
- Django admin has been updated in `farming/admin.py` and personalized with a custom `templates/admin/base_site.html` theme for a cleaner, premium Nature Basket experience.
- Existing order flow can continue to persist user orders in the normalized `Order` and `OrderItem` tables.
- The database layout is designed to align with the current aesthetic frontend and support future cart-to-checkout conversions.

## Migration

Run the following commands to build the database schema:

```bash
python manage.py makemigrations farming
python manage.py migrate
```

If you want a production-ready database, configure `DJANGO_DB_ENGINE` and other database environment variables in `organicfarming/settings.py`.

## Suggested Next Steps

1. Convert product pages to dynamic templates using `Product` and `Category` objects.
2. Migrate cart state from localStorage into `Cart`/`CartItem` for authenticated users.
3. Add server-side API endpoints to keep frontend cart and backend cart in sync.
4. Add order history pages for logged-in customers.

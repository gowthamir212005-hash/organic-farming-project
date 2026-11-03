# 🌿 Organic Farm – Online Organic Shopping Website

## 📌 Project Overview

Organic Farm is a Django-based e-commerce web application developed to provide customers with an easy and convenient way to purchase organic fruits, vegetables, dairy products, and dry fruits online.

The website allows customers to browse products, add items to their shopping cart, enter delivery details, and select a payment method. The application also provides an admin dashboard for managing products and customer orders.

## ✨ Features

- 🛒 Online shopping for organic products
- 🍎 Product categories such as Fruits, Dairy, and Dry Fruits
- 🛍️ Shopping cart management
- 👤 Customer registration and login
- 🚚 Delivery address management
- 💳 Multiple payment options:
  - Cash on Delivery (COD)
  - Google Pay
  - PhonePe
  - Card Payment
- 📦 Order management
- 🔐 Django authentication system
- 🖥️ Admin dashboard
- 📱 User-friendly website interface
- 🗄️ SQLite3 database integration

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Django | Web framework |
| HTML5 | Website structure |
| CSS3 | Website styling |
| JavaScript | Interactive functionality |
| SQLite3 | Database management |
| Bootstrap | Responsive design (if used) |

## 📂 Project Structure

```text
OrganicFarm/
│
├── manage.py
│
├── farming/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── migrations/
│
├── organicfarming/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/
│
├── db.sqlite3
│
└── README.md
```

## ⚙️ Installation and Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
```

### Step 2: Navigate to the Project Folder

```bash
cd YOUR_REPOSITORY
```

### Step 3: Install Django

```bash
py -m pip install django
```

### Step 4: Apply Database Migrations

```bash
py manage.py makemigrations
```

```bash
py manage.py migrate
```

### Step 5: Create a Superuser

```bash
py manage.py createsuperuser
```

### Step 6: Run the Development Server

```bash
py manage.py runserver
```

### Step 7: Open the Website

Visit:

http://127.0.0.1:8000/

Admin Dashboard:

http://127.0.0.1:8000/admin/

## 🎯 Project Objective

The main objective of the Organic Farm project is to develop an online platform that connects customers with organic products. It simplifies the shopping process and provides a convenient way to manage products, customers, and orders.

## 🚀 Future Enhancements

- Integration with real payment gateways
- Live order tracking
- Email notifications
- Product reviews and ratings
- Advanced product search and filtering
- Improved mobile responsiveness

## 👩‍💻 Developed By

**Gowthami R**

Project: Organic Farm

Technology: Python Django

## 📄 License

This project was developed for educational purposes.

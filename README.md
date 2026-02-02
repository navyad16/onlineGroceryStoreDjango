# 🛒 Online Grocery Store – Django Web Application

A full-stack e-commerce web application built using Django that allows users to browse groceries, manage a cart, place orders, and track delivery status with email notifications.

---

## 🚀 Features

### 👤 User Management
- User registration with email
- Secure login & logout (Django Authentication)
- Session-based cart (works without login)

### 🛍️ Product Management
- Products with categories & slugs
- Product detail page
- Stock availability check
- Admin product & category control

### 🛒 Cart & Checkout
- Add / remove / update cart items
- Session-based cart logic
- Checkout with Cash on Delivery / Online Payment
- Automatic stock reduction after order placement

### 📦 Orders & Tracking
- Order creation & order history
- Order status tracking:
  - Pending → Processing → Out for Delivery → Delivered
- Visual order progress bar
- Estimated delivery date calculation
- Auto-update delivery date when delivered
- Order cancellation with stock restoration

### 📧 Email Notifications
- Order confirmation email after checkout
- Order cancellation email
- Configurable SMTP email setup

### 🧾 Invoice
- Downloadable PDF invoice for orders

---

## 🛠️ Tech Stack

- **Backend:** Python, Django
- **Frontend:** HTML, CSS, Bootstrap
- **Database:** SQLite / MySQL
- **Email:** SMTP (Gmail)
- **Others:** Django Sessions, Django Admin

---

## 📂 Project Structure


# Online Bookstore

## Overview
The **Online Bookstore** is a comprehensive web-based platform that enables users to seamlessly browse, search, and purchase books. The platform integrates Firebase for authentication and data storage, ensuring a secure and efficient user experience.

## Features
### 1. User Authentication
- Secure signup and login using Firebase Authentication.
- Passwords stored securely in Firebase.
- Profile management with options to update email (email verification required), phone number, and password.

### 2. Book Browsing and Search
- Browse books by category.
- Search for books by title or keyword.
- View detailed book information, including description, price, and an option to add to the cart.

### 3. Shopping Cart and Checkout
- Add and remove books from the cart.
- Streamlined checkout process with multiple payment options.
- Saved addresses for quick selection during checkout.

### 4. Payment Processing
- **PhonePe QR code** for digital payments.
- **Pay on Delivery** option for convenience.
- Order confirmation and success messages displayed post-purchase.
- Automatic redirection to the homepage after a successful transaction.

### 5. Subscription Plans
- Users can choose from three premium plans that provide discounts on book purchases.
- Subscription details are securely stored in Firebase.
- Dedicated **Subscription Purchase Page** for seamless plan selection and payment.

### 6. Profile and Settings
- User profile page to manage personal details.
- Settings menu offering access to:
  - Cart
  - Profile Update
  - Addresses
  - Terms and Conditions
  - Subscriptions
  - Order History

## Tech Stack
- **Frontend:** HTML, CSS, JavaScript (Flask templating)
- **Backend:** Flask (Python)
- **Database & Authentication:** Firebase
- **Payment Processing:** PhonePe QR code, Cash on Delivery

## File Structure
```
/static
    /styles.css
/templates
    /book_details.html
    /cart.html
    /category.html
    /confirm_purchase.html
    /index.html
    /login.html
    /purchase.html
    /search.html
    /search-results.html
    /signup.html
    /profile.html
    /subscriptions.html
app.py
```

## Installation & Setup
### Prerequisites
- Python 3.x
- Firebase project setup with authentication and Firestore enabled

### Steps to Run the Application
1. **Clone the Repository:**
   ```sh
   git clone https://github.com/your-repo/online-bookstore.git
   cd online-bookstore
   ```
2. **Install Dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
3. **Configure Firebase:**
   - Create a Firebase project.
   - Enable Authentication (Email/Password) and Firestore.
   - Download the `firebase-adminsdk.json` credentials file and place it in the project folder.
4. **Run the Application:**
   ```sh
   python app.py
   ```
5. **Access the Website:**
   - Open a browser and go to `http://127.0.0.1:5000/`

## Future Enhancements
- Implement support for multiple saved addresses per user.
- Add additional payment gateways for enhanced flexibility.
- Improve UI/UX for a more intuitive shopping experience.
- Integrate AI-powered book recommendations.

## License
This project is the intellectual property of its respective owner. Unauthorized distribution or modification without prior permission is prohibited.


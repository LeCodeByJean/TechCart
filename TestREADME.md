<div style="text-align: right;">
  University of Essex Online<br>
  Module: Secure Software Development (SSD)<br>
  Tutor: Dr Cathryn Peoples<br>
  Student: Jean-G. De Souza
</div>

# TechCart 🛒

<h6 align="left">Word Count: xxxx</h6>

TechCart is a simple e-commerce platform designed to facilitate a secure shopping experience for users. This application includes features such as user registration, login, guest browsing (no account), shopping cart management, and order placement. The platform emphasizes security, data validation, and thorough testing to ensure reliability and robustness.


## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Security Focus](#security-focus)
- [Data Validation](#data-validation)
- [Testing](#testing)
- [Potential Future Implementations](#potential-future-implementations)


## Installation

To install and run TechCart, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/lecodebyjean/techcart.git
   cd techcart
   ```
3. Install the required dependencies:
   ```
   pip3 install -r requirements.txt
   ```


## Run the application:

      ### As a Customer:
      From the root TechCart, run:
      
      ```
      python3 main.py
      ```

      ### As an Administrator:
      
      ```
      python3 -m API.inventory_api
      ```


## Usage

TechCart offers a command-line interface (CLI) for users to interact with the platform. The main functionalities available through the CLI include:

- Registering a new user
- Logging in as an existing user
- Browsing available products
- Adding items to the shopping cart
- Viewing and managing the shopping cart
- Placing an order

  ### Example Commands
  
  1. Register a new user:
     ```
     python3 main.py register
     ```
  
  2. Log in as an existing user:
     ```
     python3 main.py login
     ```
  
  3. Browse products:
     ```
     python3 main.py view-items
     ```
  
  4. Add an item to the cart:
     ```
     python3 main.py add-to-cart
     ```
  
  5. View the cart:
     ```
     python3 main.py view-cart
     ```
  
  6. Checkout and place an order:
     ```
     python3 main.py checkout
     ```


## Features

  ### User Authentication
  
  - **Registration**: Users can create a new account by providing a username, email, and password. The system enforces strong password policies and validates email formats.
  - **Login**: Existing users can log in using their credentials. The system includes security measures like rate limiting and two-factor authentication (2FA) after multiple failed login attempts.
  
  ### Product Management
  
  - **Browse Products**: Users can browse available products, view details, and add items to their cart.
  - **Add to Cart**: Users can add selected products to their shopping cart, specifying the quantity.
  - **View Cart**: Users can view the items in their cart, update quantities, or remove items.
  - **Checkout**: Users can proceed to checkout, where the system calculates the total amount and processes the payment.
  
  ### Order Management
  
  - **Order Creation**: When a user places an order, the system creates an order record, processes the payment, and updates stock quantities.
  - **Order Tracking**: Users can view the status of their orders and receive updates as the status changes.
  


## Security Focus

TechCart implements several security features to protect user data and ensure secure transactions:

  ### Password Management
  
  - **Salted Password Hashing**: Passwords are hashed using SHA-256 with a unique salt for each user. This prevents attackers from using precomputed hashes to crack passwords. The use of salt in password encryption significantly enhances security by mitigating the risk of precomputed hash attacks, such as dictionary attacks. Salt adds random data to the passwords before hashing, increasing the complexity and uniqueness of the encrypted passwords. This method ensures that even if the same password is used by different users, the resulting hash values will be different, making it harder for attackers to crack the passwords (Ebanesar & Suganthi, 2019).
  - 
  - **Strong Password Requirements**: Passwords must be at least 8 characters long and include a mix of upper and lower case letters, digits, and special characters.
  
  ### Two-Factor Authentication (2FA)
  
  - **Conditional 2FA**: After three failed login attempts, the system requires users to enter a security code sent to their email. This adds an additional layer of security against unauthorized access.
  
  ### Data Encryption
  
  - **Symmetric Encryption**: Sensitive user data, such as email addresses and keys, are encrypted using the Fernet symmetric encryption algorithm. The system uses a master key to encrypt and decrypt user keys, providing an additional layer of security.
  
  ### Rate Limiting
  
  - **API Rate Limiting**: To prevent abuse and protect against denial-of-service attacks, the system limits the number of requests from a single IP address. The default limit is 200 requests per day and 50 requests per hour.



## Data Validation

Data validation is crucial to ensure the integrity and reliability of the system. TechCart employs various validation techniques:

  ### Email Validation
  
  - **Format Checking**: The system validates the format of email addresses during registration to ensure they conform to standard email address formats.
  
  ### Password Validation
  
  - **Strength Checking**: Passwords are checked to ensure they meet the required strength criteria, including length and character diversity.
  
  ### Input Sanitization
  
  - **Sanitization**: User inputs are sanitized to prevent injection attacks and ensure that data stored in the database is clean and safe.



## Testing

TechCart includes a comprehensive suite of tests to ensure the correctness and reliability of the system. The tests cover various aspects of the application, including:

  ### Unit Tests
  
  - **Functionality Testing**: Tests for individual functions and methods to ensure they perform as expected.
  - **Boundary Testing**: Tests for edge cases and boundary conditions to ensure the system handles them gracefully.
  
  ### Integration Tests
  
  - **Module Interactions**: Tests for interactions between different modules to ensure they work together correctly.
  - **Data Flow**: Tests for data flow between modules, including user authentication, shopping cart management, and order processing.
  
  ### Security Tests
  
  - **Authentication Testing**: Tests for the authentication process, including 2FA and rate limiting.
  - **Encryption Testing**: Tests for data encryption and decryption to ensure sensitive data is protected.
  
  ### Example Test Cases
  
  1. **User Registration**: Test the registration process with valid and invalid inputs.
  2. **Login Attempts**: Test login attempts with correct and incorrect credentials, including triggering 2FA.
  3. **Shopping Cart**: Test adding, updating, and removing items from the cart.
  4. **Order Placement**: Test the order placement process, including payment validation.



## Potential Future Implementations

TechCart aims to continuously improve and expand its features. Potential future implementations include:

  ### Enhanced User Experience
  
  - **Graphical User Interface (GUI)**: Develop a user-friendly GUI to replace the CLI, making it easier for users to interact with the platform.
  - **Mobile App**: Create a mobile application to provide users with on-the-go access to TechCart.
  
  ### Advanced Features
  
  - **Wishlist**: Allow users to create and manage wishlists for products they are interested in purchasing later.
  - **Recommendations**: Implement a recommendation engine to suggest products based on user behaviour and preferences.
  
  ### Improved Security
  
  - **OAuth Integration**: Integrate OAuth for secure third-party authentication, allowing users to log in using their existing social media accounts.
  - **Advanced Fraud Detection**: Implement machine learning algorithms to detect and prevent fraudulent transactions.
  
  ### Scalability and Performance
  
  - **Database Optimization**: Optimize database queries and indexing to improve performance and scalability.
  - **Load Balancing**: Implement load balancing to distribute traffic across multiple servers, ensuring high availability and reliability.



## Conclusion

TechCart is a robust and secure e-commerce platform designed to provide users with a seamless shopping experience. With its comprehensive features, stringent security measures, and thorough testing, TechCart ensures reliability and user satisfaction. Future implementations aim to enhance the platform's capabilities and user experience, making TechCart a leading solution in the e-commerce space.


## References

Ebanesar, T. and Suganthi, G. (2019). Improving Login Process by Salted Hashing Password Using SHA-256 Algorithm in Web Applications. International Journal of Computer Sciences and Engineering, 7(3), pp.27–32. doi:https://doi.org/10.26438/ijcse/v7i3.2732.


## credits

<ul>
<li>Gif from videos done with https://www.veed.io/convert/video-to-gif</li>
<li>Media stored and linked with https://www.imgbb.com</li>
</ul>

<div style="text-align: right;">
  University of Essex Online<br>
  Module: Secure Software Development (SSD)<br>
  Tutor: Dr Cathryn Peoples<br>
  Student: Jean-G. De Souza
</div>

# TechCart 🛒

<h6 align="left">Word Count: 1420 (excluding references and credits)</h6>

TechCart is a simple e-commerce platform designed to offer users a secure shopping experience. This application includes features such as user registration, login, guest browsing (no account needed), shopping cart management, payment, and order placement. TechCart also includes an API for inventory management, allowing administrators to create, read, update, and delete (CRUD) products. It was developed with an emphasis on security, data validation, and thorough testing to ensure reliability and robustness.


## Table of Contents

- [Installation](#installation)
- [Customer Usage](#customer-usage)
- [Administrator Usage](#administrator-usage)
- [Security Features](#security-features)
- [Testing](#testing)
- [Weakness and Potential Implementations](#weakness-and-potential-implementations)
- [References](#references)
- [Credits](#credits)


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


## Customer Usage:


  ### Run the Application:
  
  From the root TechCart, run:
      
  ```
  python3 main.py
  ```

  ### Usage

TechCart offers a command-line interface (CLI) for users to interact with the platform. The main functionalities available through the CLI include:

- Logging in as an existing user
- Registering as a new user
- Browsing available products as a guest
- Browsing available products as a logged-in user
- Shopping cart management (add or delete items from it)
- Viewing and managing the shopping cart
- Placing an order
- Paying (simulation)

Illustration:

![@changeBefore](https://i.ibb.co/Nr5bkyr/Screen-Recording-2024-05-25-at-2.gif)

  ### Example Use Cases
  
**Register a New User**
  To enable all functionalities of the TechCart platform, you must be a registered customer. This process will create a new account:

   ```sh
   python3 main.py
   ```

   After launching the CLI, select the option to create an account:
   - Choose option `2. Create an account`
   - Follow the prompts to enter your username, email, and a strong password as per the requirements.
   - The registration process will directly lead you to the logged-in menu with access to all available options.

**Login as an Existing User**
  If you already have an account, you can log in to access the programme features, such as managing your cart and placing orders:

   ```sh
   python3 main.py
   ```

   After launching the CLI, select the option to log in:
   - Choose option `1. Login`
   - Follow the prompts to enter your username and password.
    (only 3 attempts before the two-factor authentication process is launched)
    - The Login process will lead you to the logged-in menu with access to all available options.

**Browse as a Guest User**
   If you do not have an account and do not wish to create one, you can browse the products available on the platform as a guest user.

   ```sh
   python3 main.py
   ```

   After launching the CLI, select the option to browse as a guest:
   - Choose option `3. Browse as a guest`
   - You can then choose `1. View our available items` to view the available products and their details.


## Administrator Usage:

In this software, the administrative functions were specifically designed to be managed entirely through an API. Creating an API was a requirement for this project, but implementing it specifically for the inventory management system is a strategic decision that ensures scalability and future-proofing by preparing the system for future integration with Enterprise Resource Planning (ERP) systems like SAP or Oracle. The API allows for efficient interoperability between the inventory management system and external systems like an ERP. This not only facilitates automation and real-time data synchronization but also enables the app to easily adapt to evolving business needs.

  ### Run the Application:
  
  1-From the root TechCart, load the flask server:
      
  ```
  python3 -m API.inventory_api
  ```

  2-In a second terminal (still in the root TechCart), access the API CLI:

  ```
  python3 API/api_cli.py
  ```

  Follow the instructions from the CLI to the CRUD inventory.
  
  Note: The terminal with the flask server must remain open while using CLI.

Illustration:

![@changeBefore](https://i.ibb.co/Nr5bkyr/Screen-Recording-2024-05-25-at-2.gif)

  ### Usage

The inventory management CLI provides a simple interface for administrators to manage the inventory using the API endpoints. This CLI allows you to perform various actions:

  - Retrieve and display all products in the inventory.
  - Retrieve and display detailed information for a specific product.
  - Add a new product to the inventory.
  - Update the details of an existing product.
  - Remove a product from the inventory.

The CLI interacts with the API endpoints using the `requests` library, sending and receiving data in JSON format. The base URL for the API is `http://127.0.0.1:5000/api`.

### Example Use Cases

**Viewing All Available Items**

To view all available items, follow these steps:

In the CLI:
   - Run the CLI as instructed above.
   - Select the option to view all products by entering `1` when prompted.

   The CLI will display all products with details such as Stock Keeping Unit (SKU), name, description, price, and stock quantity.

Using a Web Browser:
   - Open your web browser.
   - Enter the following URL:
     ```
     http://127.0.0.1:5000/api/products
     ```
   This will display a JSON list of all products available in the inventory.

**Updating an Item**

To update an item using the CLI, follow these steps:

In the CLI:
   - Run the CLI as instructed above.
   - Select the option to update a product by entering `4` when prompted.
   - Enter the SKU of the product you wish to update.
   - The current product details will be displayed.
   - Enter the new product details when prompted (leave fields blank to keep current values).

   The CLI will send a request to update the product, and a response will be displayed indicating the success or failure of the operation.


## Security Features

  ### Data Encryption
  
  - **Symmetric Encryption**: Sensitive user data, such as email addresses and keys, are encrypted using the Fernet symmetric encryption algorithm. The system uses a master key to encrypt and decrypt user keys, providing an additional layer of security.

  ### Password Management
  
  - **Salted Password Hashing**: Passwords are hashed using SHA-256 with a unique salt for each user. Salt adds random data to the passwords before hashing, increasing the complexity and uniqueness of the encrypted passwords. The use of salt in password encryption significantly enhances security by mitigating the risk of precomputed hash attacks, such as dictionary attacks. This method ensures that even if the same password is used by different users, the resulting hash values will be different, making it harder for attackers to crack the passwords (Ebanesar & Suganthi, 2019).

  - **Strong Password Requirements**: Password requirements follow the "8, 4 rule" (a minimum of 8 characters that must include lowercase letters, uppercase letters, digits, and special characters).
  
  ### Two-Factor Authentication (2FA)
  
  - **Conditional 2FA**: After three failed login attempts, the system requires users to enter a security code sent to their email. This adds an additional layer of security against unauthorized access. According to recent research (Doerfler et al., 2019), delegation-based two-factor authentications are highly effective, preventing all automated bot attacks and over 92% of phishing-related attacks.
  
  ### Rate Limiting
  
  - **API Rate Limiting**: To prevent abuse and protect against denial-of-service attacks, the system limits the number of requests from a single IP address. The default limit is 200 requests per day and 50 requests per hour.

  ### Data Validation
  
  - **Email Format Checking**: The system validates the format of email addresses during registration to ensure they conform to standard email address formats.
  
  - **Password Strength Checking**: Passwords are checked to ensure they meet the required strength criteria, including length and character diversity.


## Testing

This project includes a complete suite of tests to ensure the correctness and reliability of the system. The tests cover various aspects of the programme:

  ### Unit Tests
  
  - **Functionality Testing**: Tests for individual functions and methods to ensure they perform as expected.
  - **Boundary Testing**: Tests for edge cases and boundary conditions to ensure the system handles them.
  
  ### Integration Tests
  
  - **Module Interactions**: Tests for interactions between different modules to ensure they work together correctly.
  - **Data Flow**: Tests for data flow between modules.
  
  ### Security Tests
  
  - **Authentication Testing**: Tests for the authentication process, including 2FA and rate limiting.
  - **Encryption Testing**: Tests for data encryption and decryption to ensure sensitive data is protected.
  

## Weakness and Potential Implementations:
  
  ### Improved Security and data validation

  - **API authentication Integration**: Integrate an authentication layer in the API to ensure secure access control.
  - **Credit Card Validation**: Implement the Luhn Algorithm (Modulus 10 Algorithm) to validate credit card numbers.
  - **OAuth Integration**: Integrate OAuth for secure third-party authentication, allowing users to log in using their existing social media accounts.
  - **Secure API Connection**: Encrypt data transmission to ensure secure API connection (https).
  - **Persistent Database**: Deploy a persistent database like SQL for robust data management, ensuring data persistence and integrity. (The usage of a permanent database was discouraged for this assignment)


## References

Ebanesar, T. and Suganthi, G. (2019). Improving Login Process by Salted Hashing Password Using SHA-256 Algorithm in Web Applications. International Journal of Computer Sciences and Engineering, 7(3), pp.27–32. doi:https://doi.org/10.26438/ijcse/v7i3.2732.

Doerfler, P., Thomas, K., Marincenko, M., Ranieri, J., Jiang, Y., Moscicki, A. and McCoy, D. (2019). Evaluating Login Challenges as aDefense against Account Takeover. The World Wide Web Conference on   - WWW ’19. doi:https://doi.org/10.1145/3308558.3313481.

## credits

<ul>
<li>Gif from videos done with https://www.veed.io/convert/video-to-gif</li>
<li>Media stored and linked with https://www.imgbb.com</li>
<li>README formatting inspired by: https://github.com/RichardLitt/standard-readme?tab=readme-ov-file</li>
</ul>

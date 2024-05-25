"""
This script provides a CLI for interacting with the API.

The CLI allows users to perform the following actions:
1. View all products
2. View product details
3. Add a new product
4. Update a product
5. Delete a product
6. Exit

The user can select an action by entering the corresponding number. The CLI
sends requests to the API to perform the selected action.

The requests are sent using the requests library, which allows the CLI to
interact with the API endpoints. The base URL for the API is set to
'http://127.0.0.1:5000/api'.

The CLI provides a simple interface for managing the inventory using the API
endpoints. It demonstrates how to interact with the API to perform
CRUD operations on the inventory data.

To run the CLI, execute the script in a terminal or command prompt. The user
can select the desired action by entering the corresponding number. The CLI
will display the results of the selected action, such as product information or
status messages.
"""
import requests

BASE_URL = 'http://127.0.0.1:5000/api'

def show_menu():
    """
    Displays the main menu of the CLI with the available actions.
    The user can select an action by entering the corresponding number.
    """
    print("\nWelcome to inventory management - CLI")
    print("1. View all products")
    print("2. View product details")
    print("3. Add a new product")
    print("4. Update a product")
    print("5. Delete a product")
    print("6. Exit")

def view_all_products():
    """
    Retrieves and displays all products from the API.
    
    The products are retrieved by sending a GET request to the '/products' endpoint.
    The response is expected to be in JSON format, containing a list of products.
    The product information is displayed in the console.

    If an error occurs during the request or response processing, an error message is displayed.
    """
    response = requests.get(f'{BASE_URL}/products', timeout=10)
    if response.status_code == 200:
        try:
            products = response.json()
            for product in products:
                print(
                    f"SKU: {product['SKU']}, Name: {product['name']}, "
                    f"Description: {product['description']}, Price: {product['price']}, "
                    f"Quantity: {product['stock']}"
                )
        except requests.exceptions.JSONDecodeError:
            print("Error: Unable to decode response. Not JSON format.")
    else:
        print(f"Error: Unable to retrieve products. Status code: {response.status_code}")

def view_product_details():
    """
    Retrieves and displays details of a specific product from the API.
    
    The user is prompted to enter the product ID (SKU) of the product they want to view.
    A GET request is sent to the '/products/{product_id}' endpoint to retrieve the product details.
    The response is expected to be in JSON format, containing the product information.
    The product details are displayed in the console.

    If the product is not found or an error occurs during the request or response processing,
    an error message is displayed.
    """
    product_id = input("Enter product ID: ")
    response = requests.get(f'{BASE_URL}/products/{product_id}', timeout=10)

    if response.status_code == 200:
        try:
            product = response.json()
            print(product)
        except requests.exceptions.JSONDecodeError:
            print("Error: Unable to decode response. Not JSON format.")
    elif response.status_code == 404:
        print("Error: Product not found.")
    else:
        print(f"Error: Unable to retrieve product details. Status code: {response.status_code}")


def add_product():
    """
    Adds a new product to the inventory by sending a POST request to the API.
    
    The user is prompted to enter the product details, including 
    name, description, price, and quantity.
    The SKU (product ID) is generated automatically by the API.
    The product details are sent in JSON format as the request body to
    the '/products' endpoint.
    The response from the API is displayed in the console, indicating the
    success or failure of the operation.
    
    If an error occurs during the request or response processing, an error message is displayed.
    """
    product = {
        "name": input("The SKU will be generated automatically. Enter product name: "),
        "description": input("Enter product description: "),
        "price": float(input("Enter product price: ")),
        "stock": int(input("Enter product quantity: "))
    }
    response = requests.post(f'{BASE_URL}/products', json=product, timeout=10)
    print(response.json())

def update_product():
    """
    Updates an existing product in the inventory by sending a PUT request to the API.

    The user is prompted to enter the SKU (product ID) of the product they want to update.
    The current product details are fetched from the API using a GET request to the
    '/products/{product_id}' endpoint.
    The user is then prompted to enter the new product details, including name, description,
    price, and quantity.
    The updated product details are sent in JSON format as the request body to the
    '/products/{product_id}' endpoint.
    The response from the API is displayed in the console, indicating the success or failure
    of the operation.

    If the product is not found, an error message is displayed.
    If an error occurs during the request or response processing, an error message is displayed.
    """
    product_id = input("Enter product SKU: ")

    # Fetch the existing product details
    response = requests.get(f'{BASE_URL}/products/{product_id}', timeout=10)

    if response.status_code == 200:
        try:
            product = response.json()
            print("Current product information:")
            print(f"Name: {product.get('name')}")
            print(f"Description: {product.get('description')}")
            print(f"Price: {product.get('price')}")
            print(f"Quantity: {product.get('stock')}")

            # Prompt user for new information
            updated_product = {
                "name":input("Enter new product name (leave blank to keep current): ") or product.get('name'),
                "description": input("Enter new product description (leave blank to keep current): ") or product.get('description'),
                "price": input("Enter new product price (leave blank to keep current): ") or product.get('price'),
                "stock": input("Enter new product quantity (leave blank to keep current): ") or product.get('stock')
            }

            # Convert price and qty to their respective types
            updated_product['price'] = float(updated_product['price'])
            updated_product['stock'] = int(updated_product['stock'])

            # Send the update request
            response = requests.put(f'{BASE_URL}/products/{product_id}', json=updated_product, timeout=10)
            print(response.json())

        except requests.exceptions.JSONDecodeError:
            print("Error: Unable to decode response. Not JSON format.")
    elif response.status_code == 404:
        print("Error: Product not found.")
    else:
        print(f"Error: Unable to retrieve product details. Status code: {response.status_code}")


def delete_product():
    """
    Deletes an existing product from the inventory by sending a DELETE request to the API.

    The user is prompted to enter the SKU (product ID) of the product they want to delete.
    A DELETE request is sent to the '/products/{product_id}' endpoint to delete the product.
    The response from the API is displayed in the console, indicating the success or failure
    of the operation.

    If the product is not found, an error message is displayed.
    If an error occurs during the request or response processing, an error message is displayed.
    """
    product_id = input("Enter product SKU: ")
    response = requests.delete(f'{BASE_URL}/products/{product_id}', timeout=10)
    print(response.json())

def main():
    """
    Main function to run the CLI.
    Displays the main menu and processes user input to perform actions.

    The user can select an action by entering the corresponding number.
    The CLI will continue to run until the user chooses to exit.

    If an invalid choice is entered, an error message is displayed.
    """
    while True:
        show_menu()
        choice = input("Enter choice: ")
        if choice == '1':
            view_all_products()
        elif choice == '2':
            view_product_details()
        elif choice == '3':
            add_product()
        elif choice == '4':
            update_product()
        elif choice == '5':
            delete_product()
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()

# End of API/api_cli.py
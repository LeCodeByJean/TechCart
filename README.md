MOST UP TO DATE VERSION

First, install the requirements.txt with the command: 

    pip3 install -r requirements.txt


##For the admin API inventory management:

1-From the root TechCart, load the flask server with the command:

    python3 -m API.inventory_api

2-In a second terminal (still in the root TechCart), access the API CLI through the command:

    python3 API/api_cli.py

note: Let the terminal with the server open during the use of CLI.
Follow the instructions from the CLI to the CRUD inventory.

This is a test with a GIF for demonstration of testing:

![](https://i.ibb.co/Nr5bkyr/Screen-Recording-2024-05-25-at-2.gif)

##For the user CLI:

From the root TechCart, run:
    python3 main.py


Password strength validation
email adress validation
two factor authentication after 3 failed attempts
user' data encryption
user's password hashed with 256 and added salt
user's credit card info hashed with 256 and added salt
Rate limit by user for cart manipulation to avoid Denial of Servie attacks
Rate Limite for API use

Future improuvements:

Implement the 'Luhn Algorithm' ('Modulus 10 Algorithm') for credit card number validation

Disclaimer:
This software is not affiliated with, endorsed by, or related to TechCart LTD or the website techcart.com.
The use of the name "TechCart" in this programme is fictional and for illustrative purposes only. It was independently conceived as a placeholder for this
assignment project, and any resemblance to actual companies or products is purely coincidental.

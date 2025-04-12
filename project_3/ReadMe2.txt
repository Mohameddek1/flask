Testing the Application
Start the Flask Server:


python app.py
Sample API Calls:

Register a user:

curl -X POST -H "Content-Type: application/json" -d '{"username": "admin", "password": "12345", "role": "Admin"}' http://127.0.0.1:5000/auth/register
Add a customer:

curl -X POST -H "Content-Type: application/json" -d '{"name": "John Doe", "email": "john@example.com"}' http://127.0.0.1:5000/customer/
Add a credit card:

curl -X POST -H "Content-Type: application/json" -d '{"customer_id": 1, "card_number": "4111111111111111", "cvv": "123", "expiry_date": "12/25"}' http://127.0.0.1:5000/card/
Retrieve the card:

curl http://127.0.0.1:5000/card/1
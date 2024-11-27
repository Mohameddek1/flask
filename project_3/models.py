from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

#initialize flask extension
db = SQLAlchemy()  # SQLAlchemy for database interactions
bcrypt = Bcrypt()  # Bcrypt for password hashing

# Function to encrypt data using AES
def aes_encrypt(data, key):
    """
    Encrypts the provided data using AES encryption (ECB mode).

    Parameters:
    - data (str): The plaintext data to encrypt.
    - key (bytes): The encryption key (must be 16, 24, or 32 bytes for AES).

    Returns:
    - bytes: Encrypted data.
    """
    cipher = Cipher(algorithms.AES(key), modes.ECB())
    encryptor = cipher.encryptor()
    # Pad data to be a multiple of 16 bytes (block size for AES)
    padded_data = data.ljust(16, ' ').encode()  # Adds spaces to the end
    return encryptor.update(padded_data)

# Function to decrypt AES-encrypted data
def aes_decrypt(encrypted_data, key):
    """
    Decrypts the provided AES-encrypted data.

    Parameters:
    - encrypted_data (bytes): The encrypted data to decrypt.
    - key (bytes): The encryption key.

    Returns:
    - str: Decrypted plaintext data.
    """
    cipher = Cipher(algorithms.AES(key), modes.ECB())
    decryptor = cipher.decryptor()
    return decryptor.update(encrypted_data).strip().decode()  # Remove padding and decode

# Define the User model for storing user credentials and roles
class User(db.Model):
    """
    Represents a system user with a username, password hash, and role.
    """
    id =db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    
    # Method to hash and store the user's password
    def set_password(self, password):
        """
        Hashes and sets the user's password.
        
        Parameters:
        - password (str): The plaintext password.
        """
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        
    
    # Method to check the provided password against the stored hash
    def check_password(self, password):
        """
        Verifies the provided password against the stored hash.

        Parameters:
        - password (str): The plaintext password to verify.

        Returns:
        - bool: True if the password matches, False otherwise.
        """
        return bcrypt.check_password_hash(self.password_hash, password)
    

# Define the Customer model for storing customer information
class Customer(db.Model):
    """
    Represents a customer with a name and email.
    """
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for the customer
    name = db.Column(db.String(120), nullable=False)  # Customer's name
    email = db.Column(db.String(120), unique=True, nullable=False)  # Unique email


# Define the CreditCard model for storing encrypted credit card details
class CreditCard(db.Model):
    """
    Represents a customer's credit card with encrypted details.
    """
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for the credit card
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)  # Link to customer
    card_number = db.Column(db.LargeBinary, nullable=False)  # Encrypted card number
    cvv = db.Column(db.LargeBinary, nullable=False)  # Encrypted CVV
    expiry_date = db.Column(db.LargeBinary, nullable=False)  # Encrypted expiry date
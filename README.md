# User Management and Financial Transactions API

This project is a Flask-based RESTful API for managing users and handling financial transactions, built on top of MongoDB and using MongoEngine as the ORM. The app includes functionalities to create, update, and verify user accounts, as well as to interact with financial endpoints for making transfers and querying balances.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)

## Features

- **User Management**: Create, retrieve, update, and delete user accounts.
- **Financial Transactions**: Integration with Squad API to facilitate payments, account lookups, and balance retrieval.
- **Data Storage**: User data is stored in MongoDB with MongoEngine for schema modeling.
- **Blueprint-based Routing**: Separate modules for `user` and `transfer` routes.
- **Security**: Password hashing with bcrypt and unique user IDs for account verification.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name

2. Set up a virtual environment:
   ```bash
    python3 -m venv venv
    source venv/bin/activate
   
3. Install dependencies:
    ```bash
    pip install -r requirements.txt

4. Configure environment variables (e.g., SECRET_KEY for Flask).
   
5. Start MongoDB and Flask server:
     ````bash
     mongod --dbpath /path/to/your/db
     python app.py

## Usage

1. Start the Flask application:
   ```bash
   flask run

## API Endpoints

User Endpoints (/api/user)
- **POST** /create: Register a new user.
- **POST** /verify: Verify user and create a virtual account.
- **POST** /details: Retrieve user details.
- **POST** /balance: Retrieve user balance.

##Transfer Endpoints (/api/transfer)
- **POST** /make-transfer: Initiate a financial transfer.
  

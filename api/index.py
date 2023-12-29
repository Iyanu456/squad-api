from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_wtf.csrf import CSRFProtect
from mongoengine import NotUniqueError
from Models.models import User, StorageEngine
import requests
from datetime import datetime, date

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
storage_engine = StorageEngine('squidDB', 'localhost', 27017)


urls = {
    "create_merchant": "https://sandbox-api-d.squadco.com/merchant/create-sub-users",
    "create_virtual_acct": "https://sandbox-api-d.squadco.com/virtual-account",
    "payments": "https://sandbox-api-d.squadco.com/transaction/initiate",
    "transfer": "https://sandbox-api-d.squadco.com/payout/account/lookup",
    "wallet_balance": "https://sandbox-api-d.squadco.com/merchant/balance"
}


# Function to make a POST request to the endpoint
def make_post_request(endpoint, user_data):

    authorization_token = "sandbox_sk_25c04c9060872f1e36b823021c2984a32cbf29596d58"
    headers = {
        "Authorization": f"Bearer {authorization_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(endpoint, json=user_data, headers=headers)
    return response



@app.route('/api/user', methods=['POST'])
def create_user():

    try:

        data = request.json
        user = User.objects(email=data.get('email')).first()

        if user:
            response_data = {"message": "User already exist"}
            return jsonify(response_data), 201

        else:
            new_user = User(
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                username=data.get('username'),
                email=data.get('email'),
                password=data.get('password'),
                phone_number=data.get('phone_number'),
            )

            # Save the form data to the database
            new_user.save()

            response_data = {"message": "User created successfully"}
            return jsonify(response_data), 201
    
    except NotUniqueError as e:
        # Handle the unique constraint violation
        response_data = {"error": f"An error occurred: {e}"}
        return jsonify(response_data), 500



    
@app.route('/api/user/verify', methods=['POST'])
def verify_user():

    try:

        data = request.json

        # Retrieve the user by user_id
        user = User.objects(email=data.get('email')).first()

        if user:
            # Update the user with additional details
            user.dob = data.get('dob')
            user.address = data.get('address')
            user.phone_number = data.get('phone_number')  # New field
            user.is_verified = True  # Mark the user as verified
            gender = data.get('gender')
            if gender == "male":
                user.gender = "1"
            else:
                user.gender = "2"
            user.save()

            # Return a JSON response
            response_data = {"message": "User details updated successfully (Second Stage)"}
            return jsonify(response_data), 200
        
        else:
            response_data = {"error": "User not found"}
            return jsonify(response_data), 404
        
    except Exception as e:
        # Handle other exceptions
        response_data = {"error": f"An error occurred: {e}"}
        return jsonify(response_data), 500
    

if __name__ == "__main__":
    # Enable debug mode
    app.run(debug=True)

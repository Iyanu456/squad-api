from flask import Flask, render_template, request, redirect, url_for, jsonify, json
#from flask_wtf import FlaskForm
#from wtforms import StringField, PasswordField, SubmitField
#from wtforms.validators import DataRequired, Email
#from flask_wtf.csrf import CSRFProtect
from mongoengine import NotUniqueError
from Models.models import User, StorageEngine
from functions import make_post_request, create_virtual_account
import requests
from datetime import datetime, date

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
storage_engine = StorageEngine('squidDB', 'localhost', 27017)


urls = {
    "merchant_url": "https://sandbox-api-d.squadco.com/merchant/create-sub-users",
    "virtual_acct_url": "https://sandbox-api-d.squadco.com/virtual-account",
    "payments_url": "https://sandbox-api-d.squadco.com/transaction/initiate",
    "transfer_url": "https://sandbox-api-d.squadco.com/payout/account/lookup",
    "wallet_url": "https://sandbox-api-d.squadco.com/merchant/balance"
}


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
                role=data.get('role')
            )

            # Save the form data to the database
            new_user.save()

            response_data = {
                "message": "User created successfully",
                "status": 201,
                }
            return jsonify(response_data), 201
    
    except NotUniqueError as e:
        # Handle the unique constraint violation
        response_data = {
            "error": f"An error occurred: {e}",
            "message": "This user already exist",
            "status": 500,
            }
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
            user.role = data.get('role')  # New field
            gender = data.get('gender')
            if gender:
                if gender == "male":
                    user.gender = "1"
                else:
                    user.gender = "2"

            user.save()

            if user.role == "basic" and user.is_verified == True:
                data = {
                    "customer_identifier": str(user.user_id),
                    "first_name": f"Iyanuoluwa-{str(user.first_name)}",
                    "last_name": str(user.last_name),
                    "mobile_num": str(user.phone_number),
                    "email": str(user.email),
                    "bvn": str(user.bvn_no),
                    "dob": user.dob,
                    "address": str(user.address),
                    "gender": str(user.gender),
                    }
                
                response_data = create_virtual_account(data, user.role)
                return jsonify(response_data.json()), 200
                
            if user.role == "merchant" and user.is_verified == True:
                data = {
                    "customer_identifier": str(user.user_id),
                    "business_name": f"Iyanuoluwa- {str(user.business_name)}",
                    "mobile_num": str(user.phone_number),
                    "bvn": str(user.bvn_no),
                    }
                
                response_data = create_virtual_account(data, user.role)
                return jsonify(response_data.json()), 200
        
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

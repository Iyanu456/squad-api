# /blueprints/user.py
from flask import Blueprint, jsonify, request
from mongoengine import NotUniqueError
from Models.models import User
from functions.create_virtual_acct import create_virtual_account
from functions.make_requests import make_get_request, make_post_request
import bcrypt
from datetime import datetime

user_blueprint = Blueprint('user', __name__)

urls = {
    "merchant_url": "https://sandbox-api-d.squadco.com/merchant/create-sub-users",
    "virtual_acct_url": "https://sandbox-api-d.squadco.com/virtual-account",
    "wallet_url": "https://sandbox-api-d.squadco.com/merchant/balance",
    "virtual_acct_details_url": "https://sandbox-api-d.squadco.com/virtual-account/",
    "get_balance_url": "https://sandbox-api-d.squadco.com/merchant/balance"
}

@user_blueprint.route('/create', methods=['POST'])
def create_user():
    try:
        data = request.json
        user = User.objects(email=data.get('email')).first()

        if user:
            response_data = {"message": "User already exists"}
            return jsonify(response_data), 201

        else:
            new_user = User(
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                email=data.get('email'),
                password=bcrypt.hashpw(data.get('password').encode('utf-8'), bcrypt.gensalt()),
                phone_number=data.get('phone_number'),
                role=data.get('role')
            )
            new_user.save()

            response_data = {
                "message": "User created successfully", 
                "status": 201
                }
            return jsonify(response_data), 201

    except NotUniqueError as e:
        response_data = {
            "error": f"An error occurred: {e}", 
            "message": "This user already exists", 
            "status": 500
            }
        return jsonify(response_data), 500

    except Exception as e:
        response_data = {
            "error": f"An error occurred: {e}", 
            "message": "Operation failed", 
            "status": 500
            }
        return jsonify(response_data), 500

@user_blueprint.route('/verify', methods=['POST'])
def verify_user():
    try:
        data = request.json
        user = User.objects(email=data.get('email')).first()

        if user:
            # Update user details and mark as verified
            user.dob = datetime.strptime(data.get('dob'), '%d/%m/%Y')
            user.address = data.get('address')
            user.phone_number = data.get('phone_number')
            user.is_verified = True
            user.bvn_no = str(bcrypt.hashpw(data.get('bvn_no').encode('utf-8'), bcrypt.gensalt()))

            gender = data.get('gender')
            if gender:
                if gender == "male":
                    user.gender = "1"
                else:
                    user.gender = "2"

            if data.get('username'):
                user.username = data.get('username')

            user.save()

            # Additional details and create virtual account logic here...
            if user.role == "basic" and user.is_verified == True:
                data = {
                    "user_id": str(user.user_id),
                    "first_name": f"Iyanuoluwa-{user.first_name}",
                    "last_name": user.last_name,
                    "mobile_num": user.phone_number,
                    "email": user.email,
                    "bvn_no": f"{str(data.get('bvn_no'))}",
                    "dob": user.dob.strftime('%d/%m/%Y'),
                    "address": user.address,
                    "gender": user.gender,
                    }
                
                response_data = create_virtual_account(data, urls, user.role)
                return response_data

            elif user.role == "merchant" and user.is_verified == True:
                data = {
                    "user_id": str(user.user_id),
                    "business_name": f"Iyanuoluwa- {user.business_name}",
                    "mobile_num": user.phone_number,
                    "bvn_no": f"{str(data.get('bvn_no'))}",
                    }
                
                response_data = create_virtual_account(data, urls, user.role)
                return response_data

        else:
            response_data = {"error": "User not found"}
            return jsonify(response_data), 404

    except Exception as e:
        response_data = {
            "error": f"An error occurred: {e}", 
            "message": "Operation failed", 
            "status": 500
            }
        return jsonify(response_data), 500

@user_blueprint.route('/details', methods=['POST'])
def retrieve_user_detail():
    data = request.json
    user_id = data.get('user_id')
    try:
        response = make_get_request(urls['virtual_acct_details_url'] + user_id )
        return response

    except Exception as e:
        return response

@user_blueprint.route('/balance', methods=['POST'])
def retrieve_user_balance():
    #data = request.json
    params = {"currency_id": "NGN"}

    try:
        response = make_get_request(urls['get_balance_url'], params)
        return response

    except Exception as e:
        return response

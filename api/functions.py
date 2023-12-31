from flask import json, jsonify
from Crypto.Cipher import AES
import requests
from base64 import b64encode, b64decode

# Function to make a POST request to the endpoint
def make_post_request(endpoint, user_data):

    authorization_token = "sandbox_sk_25c04c9060872f1e36b823021c2984a32cbf29596d58"
    headers = {
        "Authorization": f"Bearer {authorization_token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(endpoint, json=user_data, headers=headers)
        return response.json()

    except Exception as e:
        return response


def make_get_request(url, params=None):
    """
    Make a GET request to the specified URL.

    Parameters:
    - url (str): The URL to make the GET request to.
    - params (dict, optional): Query parameters to include in the request.
    - headers (dict, optional): Headers to include in the request.

    Returns:
    - dict: The JSON response or an empty dictionary if the response is not JSON.
    """
    authorization_token = "sandbox_sk_25c04c9060872f1e36b823021c2984a32cbf29596d58"
    headers = {"Authorization": f"Bearer {authorization_token}"}

    try:
        response = requests.get(url, params=params, headers=headers)

        # Check if the request was successful (status code 200)
        response.raise_for_status()

        # Try to parse the response as JSON
        try:
            json_response = response.json()
            return json_response
        except ValueError:
            # Response is not JSON, return an empty dictionary
            return {}

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during GET request: {e}")
        # You might want to handle the exception differently based on your needs
        return {}


def check_password(password, secretKey, encrypted_password):
    cipher = AES.new(secretKey.encode('utf-8'), AES.MODE_EAX)
    nonce = b64decode(encrypted_password["nonce"])
    ciphertext = b64decode(encrypted_password["ciphertext"])
    cipher.set_nonce(nonce)
    decrypted_password = cipher.decrypt(ciphertext).decode('utf-8')
    return decrypted_password == password

def create_virtual_account(user, urls, role="basic"):
    try:

        if role == "basic":
           
           data = {
                "customer_identifier": user.get('user_id'),
                "first_name": user.get('first_name'),
                "last_name": user.get('last_name'),
                "mobile_num": user.get('mobile_num'),
                "email": user.get('email'),
                "bvn": user.get('bvn_no'),
                "dob": user.get('dob'),
                "address": user.get('address'),
                "gender": user.get('gender'),
            }
        elif role == "merchant":
            data = {
                "customer_identifier": user.get('user_id'),
                "business_name": user.get('business_name'),
                "mobile_num": user.get('mobile_num'),
                "bvn": user.get('bvn_no'),
            }

        
        response_data = make_post_request(urls["virtual_acct_url"], data)
        return jsonify(response_data), response_data.get('status')

    except Exception as e:

        # Handle other exceptions
        response_data = {
            "error": f"(Api) - An error occurred: {e}",
            "message": "Operation failed",
            "status": 500,
            }
        return jsonify(response_data), 500
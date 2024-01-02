from flask import jsonify
from .make_requests import make_post_request


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
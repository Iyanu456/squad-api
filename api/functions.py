# Function to make a POST request to the endpoint
def make_post_request(endpoint, user_data):

    authorization_token = "sandbox_sk_25c04c9060872f1e36b823021c2984a32cbf29596d58"
    headers = {
        "Authorization": f"Bearer {authorization_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(endpoint, json=user_data, headers=headers)
    return response

def create_virtual_account(user, role="basic"):
    try:

        if role == "basic":
            data = {
                "customer_identifier": user[user_id],
                "first_name": user[first_name],
                "last_name": user[last_name],
                "mobile_num": user[phone_number],
                "email": user[email],
                "bvn": user[bvn_no],
                "dob": user[dob],
                "address": user[address],
                "gender": user[gender],
                }
            
        if role == "merchant":
            data = {
                "customer_identifier": user[user_id],
                "business_name": user[business_name],
                "mobile_num": user[phone_number],
                "bvn": user[bvn_no],
                }

        
        response_data = make_post_request(urls["virtual_acct_url"], data)
        return jsonify(response_data.json()), 200

    except Exception as e:

        # Handle other exceptions
        response_data = {
            "error": f"An error occurred: {e}",
            "message": "Operation failed",
            "status": 500,
            }
        return jsonify(response_data), 500
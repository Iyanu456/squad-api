from flask import json
import requests

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
        json_response = response.json()

        return json_response

    except Exception as e:
        print(f"An error occurred during GET request: {e}")
        # You might want to handle the exception differently based on your needs
        return response.json()
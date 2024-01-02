# /blueprints/transfer.py
from flask import Blueprint, jsonify, request
from functions.make_requests import make_post_request

transfer_blueprint = Blueprint('transfer', __name__)

urls = { 
    "payments_url": "https://sandbox-api-d.squadco.com/transaction/initiate",
    "acct_lookup_url": "https://sandbox-api-d.squadco.com/payout/account/lookup",
}


@transfer_blueprint.route('/make-transfer', methods=['POST'])
def make_transfer():
    data = request.json
    #bank = data.get('bank')

    user_data = {
        "bank_code": data.get('bank_code'),
        "account_number": data.get('account_number'),
    }

    try:
        response = make_post_request(urls['acct_lookup_url'], user_data)
        return response

    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500

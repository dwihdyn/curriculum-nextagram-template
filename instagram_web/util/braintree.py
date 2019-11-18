# server (backend) setup snippet from braintree : https://developers.braintreepayments.com/start/hello-server/python

import braintree
from config import BT_MERCHANT_ID, BT_PUBLIC_KEY, BT_SECRET_KEY

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id=BT_MERCHANT_ID,
        public_key=BT_PUBLIC_KEY,
        private_key=BT_SECRET_KEY
    )
)


# donation token for every different picture
def generate_client_token():
    return gateway.client_token.generate()


# details of the donations | nonce is a secure payment method
def complete_transaction(nonce, amount):
    result = gateway.transaction.sale({
        "amount": amount,
        "payment_method_nonce": nonce,
        "options": {
            "submit_for_settlement": True
        }
    })

    # breakpoint()

    # if payment failed, return False, else True
    if not result.is_success:
        return False

    return True

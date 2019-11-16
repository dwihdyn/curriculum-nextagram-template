# server (backend) setup snippet from braintree : https://developers.braintreepayments.com/start/hello-server/python

import braintree
from config import BT_MERCHANT_ID, BT_PUBLIC_KEY, BT_SECRET_KEY

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id="BT_MERCHANT_ID",
        public_key="BT_PUBLIC_KEY",
        private_key="BT_SECRET_KEY"
    )
)


def generate_client_token():
    pass

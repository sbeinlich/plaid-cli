import plaid
import os
import time

from http import HTTPStatus
from flask import Flask, render_template, request, jsonify

from plaid.api import plaid_api
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.products import Products
from plaid.model.country_code import CountryCode

import token_store

app = Flask(__name__)

plaid_config = plaid.Configuration(
  host=plaid.Environment.Sandbox,
  api_key={
    'clientId':  os.environ.get('PLAID_CLIENT_ID'),
    'secret': os.environ.get('PLAID_SECRET'),
  }
)
api_client = plaid.ApiClient(plaid_config)
client = plaid_api.PlaidApi(api_client)

# TODO: make env variable
PLAID_REDIRECT_URI = 'http://localhost:3000/'

@app.route("/")
def home():
    return render_template('index.html')


@app.route("/create_link_token", methods=['POST'])
def create_link_token():
    link_token_request = LinkTokenCreateRequest(
            products=[Products("auth")],
            client_name="Plaid Test App",
            country_codes=[CountryCode('US')],
            # redirect_uri=PLAID_REDIRECT_URI,  # TODO: implement OAuth?
            language='en',
            # Use a placeholder user ID, as we only support 1 user per CLI
            user=LinkTokenCreateRequestUser(
                client_user_id=str(time.time())
            )
        )

    response = client.link_token_create(link_token_request)
    return jsonify(response.to_dict())


@app.route('/exchange_public_token', methods=['POST'])
def exchange_public_token():
    public_token = request.form['public_token']
    exchange_token_request = ItemPublicTokenExchangeRequest(
        public_token=public_token
    )
    response = client.item_public_token_exchange(exchange_token_request)
    access_token = response['access_token']
    item_id = response['item_id']
    # TODO: encrypt and write access token to persistent storage
    token_store.add_token(access_token)

    return ('', HTTPStatus.NO_CONTENT)

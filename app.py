import re
import os

from flask import Flask
from flask_ask import Ask, statement, question, session

import requests

app = Flask(__name__)
ask = Ask(app, '/')
headers = { 'authorization': "Bearer 1669926f-c367-6f58-5027-31512f1661eb",'cache-control': "no-cache"}

nextOpenOrderUrl = "https://api.clover.com/v3/merchants/3S2JC4YEV2XTE/orders?limit=1&status=open"
BASE_URL = "https://api.clover.com/v3/merchants/3S2JC4YEV2XTE/"
lineItems = []

@ask.intent('getNextItems')
def getNextLineItems():
	orderID = getNextOrder()
	openLineItemsUrl = f'{BASE_URL}orders/{orderID}/line_items'
	lineItem_names = set()
	elements = requests.request("GET", openLineItemsUrl, headers=headers).json()
	for element in elements['elements']:
		lineItems.append(element['name'])
	lineItem_names = list(lineItem_names)
	lineItems_str = ', '.join(lineItems[:-1])
	lineItems_str += f', and {lineItems[-1]}' 
	print(lineItems_str)
	return statement(f'The items in the next order are {lineItems_str}') 

def getNextOrder():
	return requests.request("GET", nextOpenOrderUrl, headers=headers).json()['elements'][0]['id']

# Hey Alexa, how many orders have we closed today? 

# Hey Alexa, how many open orders do we have?

# Hey Alexa, what's in the next open order?

# response = requests.request("GET", openLineItemsUrl, headers=headers)
# getLineItems()

if __name__ == '__main__':
	# port = int(os.environ.get("PORT", 443))
	# app.run(debug=True, host='0.0.0.0', port=port)
	app.run()
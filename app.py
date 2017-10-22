import re

from flask import Flask
from flask_ask import Ask, statement, question, session

import requests

app = Flask(__name__)
ask = Ask(app, '/')
headers = { 'authorization': "Bearer 1669926f-c367-6f58-5027-31512f1661eb",'cache-control': "no-cache"}

lineItems = []

@ask.intent('getNextItems')
def getLineItems():
	elements = requests.request("GET", openLineItemsUrl, headers=headers).json()['elements']
	# for element in elements:
	# 	lineItems.append(element['name'])
 #    lineItems_str = ', '.join(lineItems[:-1])
 #    lineItems_str += f', and {lineItems[-1]}' 
	return statement(f'The items in the next order are ') #{lineItems_str}') 

nextOpenOrderUrl = "https://api.clover.com/v3/merchants/3S2JC4YEV2XTE/orders?limit=1&status=open"
openLineItemsUrl = "https://api.clover.com/v3/merchants/3S2JC4YEV2XTE/orders/GQV74AGX3NEG0/line_items"


# Hey Alexa, how many orders have we closed today? 

# Hey Alexa, how many open orders do we have?

# Hey Alexa, what's in the next open order?



response = requests.request("GET", openLineItemsUrl, headers=headers)

print("hello")

if __name__ == '__main__':
    app.run(host= '0.0.0.0')
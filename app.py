import re
import os
import random

from flask import Flask
from flask_ask import Ask, statement, question, session

import requests

app = Flask(__name__)
ask = Ask(app, '/')
headers = { 'authorization': "Bearer 1669926f-c367-6f58-5027-31512f1661eb",'cache-control': "no-cache"}

# nextOpenOrderUrl = "https://api.clover.com/v3/merchants/3S2JC4YEV2XTE/orders?limit=1"
BASE_URL = "https://api.clover.com/v3/merchants/3S2JC4YEV2XTE/"
# /3S2JC4YEV2XTE/tags/KW3TE8QSB4FYE/items

@ask.intent('getNextItems')
def getNextLineItems():
	orderID = getNextOrder()
	openLineItemsUrl = f'{BASE_URL}orders/{orderID}/line_items'
	lineItems_str = parseElements(openLineItemsUrl)
	print(lineItems_str) 
	return statement(f'The items in the next order are {lineItems_str}') 

def getNextOrder():
	return requests.request("GET", f'{BASE_URL}orders?limit=1', headers=headers).json()['elements'][0]['id']

def parseElements(url):
	lineItems = []
	lineItem_names = set()
	elements = requests.request("GET", url, headers=headers).json()
	for element in elements['elements']:
		lineItems.append(element['name'])
	lineItem_names = list(lineItem_names)
	lineItems_str = ', '.join(lineItems[:-1])
	lineItems_str += f', and {lineItems[-1]}' 
	return lineItems_str

@ask.intent('highPerformers')
def highPerformers():
	return statement('We\re killing it. In the past 12 hours your top items have been George\'s Classic Frozen Banana and Hot Cop Special. Raise the price of high performing items by twenty percent by saying Raise Prices.')
	
@ask.intent('lowPerformers')
def lowPerformers():
	return statement('We\ve made a huge mistake. In the past 12 hours your least performant item has been the Banana MudBone Supreme. Lower the price of low performing items by twenty percent by saying Lower Prices.')

	# In the past 12 hours your top items have been George's Classic Frozen Banana and Hot Cop Special. 
	# Do you want to raise the price of these items by twenty percent? 
	# yes -> OK! Let's make it rain. Refresh the customer app to see the new prices"
	# no -> OK! Your current prices seem to be working well. 

	# In the past 12 hours your least performant item has been the Banana MudBone Supreme. 
	# Do you want to lower the price of these items by twenty percent? 
	# yes -> OK! Let's move these products. Refresh the customer app to see the new prices"
	# no -> OK! Let's try to move these items another way. 	

# print(getNextOrder())

# getNextLineItems()

# print(getRandomItems())

if __name__ == '__main__':
	port = int(os.environ.get("PORT", 443))
	app.run(debug=True, host='0.0.0.0', port=port)
	# app.run()
import re
import os
import random

from flask import Flask
from flask_ask import Ask, statement, question, session

import requests

app = Flask(__name__)
ask = Ask(app, '/')
headers = { 'authorization': "Bearer 1669926f-c367-6f58-5027-31512f1661eb",'cache-control': "no-cache"}
BASE_URL = "https://api.clover.com/v3/merchants/3S2JC4YEV2XTE/"

@ask.intent('getNextItems')
def getNextLineItems():
	# orderID = 'getNextOrder()'
	# openLineItemsUrl = f'{BASE_URL}orders/{orderID}/line_items'
	# lineItems_str = parseElements(openLineItemsUrl)
	# print(lineItems_str) 
	# return statement(f'The items in the next order are {lineItems_str}')
	# hardcoding for demo purposes only 
	return statement('The items in the next order are Busters Mother-lovin Banana and Choco-Smothered Banana') 

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
	return statement('We are killing it. In the past 12 hours your top items have been George\'s Classic Frozen Banana and Hot Cop Special. Raise the price of high performing items by twenty percent by saying food truck app, Raise Prices.')
	
@ask.intent('lowPerformers')
def lowPerformers():
	return statement('We have made a huge mistake. In the past 12 hours your least performant item has been the Banana MudBone Supreme. Lower the price of low performing items by twenty percent by saying food truck app, Lower Prices.')
	
def getItemPrice(itemID):
	return requests.request("GET", f'{BASE_URL}items/{itemID}', headers=headers).json()['price']

def getItemName(itemID):
	return requests.request("GET", f'{BASE_URL}items/{itemID}', headers=headers).json()['name']

def dollarsAndCents(amount):
	return f'{int(str(amount)[2:])} dollars and {int(str(amount)[:2])} cents'

def raiseItemPrice(itemID):
	old_price = getItemPrice(itemID)
	new_price = int(float(getItemPrice(itemID))*1.2)
	payload = '{"price":"' + str(new_price) + '"}'
	requests.request("POST", f'{BASE_URL}items/{itemID}', headers=headers, data=payload)
	return f'The price of {getItemName(itemID)} rose from {dollarsAndCents(old_price)} to {dollarsAndCents(new_price)}'
	
def lowerItemPrice(itemID):
	old_price = getItemPrice(itemID)
	new_price = int(float(getItemPrice(itemID))*.8)
	payload = '{"price":"' + str(new_price) + '"}'
	requests.request("POST", f'{BASE_URL}items/{itemID}', headers=headers, data=payload)
	return f'The price of {getItemName(itemID)} fell from {dollarsAndCents(old_price)} to {dollarsAndCents(new_price)}'
	
@ask.intent('raisePrices')
def raiseHardCodedItems():
	frozenBanana = raiseItemPrice('33WAPCMCR5Z1Y')
	hotCop = raiseItemPrice('KRFZRYVY7JGK0')
	print(f'Make it rain. {frozenBanana}. {hotCop}.')
	return statement(f'Make it rain. {frozenBanana}. {hotCop}.')

@ask.intent('lowerPrices')
def lowerHardCodedItems():
	mudBone = lowerItemPrice('JKDDN6XGBDBVP')
	print(f'Move those products. {mudBone}.')
	return statement(f'Move those products. {mudBone}.')

if __name__ == '__main__':
	port = int(os.environ.get("PORT", 443))
	app.run(debug=True, host='0.0.0.0', port=port)
	# app.run()
import requests
import json
import math
import logging as log
import copy
import sys

TEMPLATE =  {
  "name": "Name",
  "author": "Etaro",
  "calls": [],
  "responses": []}


# return of the function getDeck
def getDeck(code):
  url = 'https://decks.rereadgames.com/api/decks/' + code
  response = requests.get(url)
  if response.status_code == 200:
    return response.json()
  else:
    return None

def mergedecks(deck1, deck2):
  # add calls and responses from deck2 to deck1
  for call in deck2['calls']:
    deck1['calls'].append(call)
  for response in deck2['responses']:
    deck1['responses'].append(response)
  return deck1

def split(arr, size):
     arrs = []
     while len(arr) > size:
         pice = arr[:size]
         arrs.append(pice)
         arr   = arr[size:]
     arrs.append(arr)
     return arrs

def splitdeck(deck):
  maxcalls = 500
  maxresponses = 1500

  if len(deck['calls']) < maxcalls or len(deck['responses']) < maxresponses:
    return [deck]
  
  callsperdeck = math.ceil(len(deck['calls']) / maxcalls)
  responsesperdeck = math.ceil(len(deck['responses']) / maxresponses)
  log.info('Calls per deck: ' + str(callsperdeck) + ' Responses per deck: ' + str(responsesperdeck))
  returndeck = []
  loopnumber = callsperdeck if callsperdeck >= responsesperdeck else responsesperdeck
  
  for i in range(1, loopnumber+1):
    temp = copy.deepcopy(TEMPLATE)
    temp['name'] = deck['name'] + ' - ' + str(i)
    temp['author'] = deck['author']
    temp['calls'] = deck['calls'][(i-1)*maxcalls:i*maxcalls]
    temp['responses'] = deck['responses'][(i-1)*maxresponses:i*maxresponses]
    
    returndeck.append(temp)
  return returndeck


def dumpdeck(maindeck):
  lastdeck = copy.deepcopy(TEMPLATE)
  for deck in maindeck:
    filesize = (sys.getsizeof(json.dumps(deck)) - sys.getsizeof(""))/1024
    log.info('Saving deck: ' + deck['name'])
    log.info('Calls: ' + str(len(deck['calls'])) + ' Responses: ' + str(len(deck['responses'])))
    log.info('Saving to file: ' + deck['name'] + '.deck.json5' + ' | Size: ' + str(filesize) + ' KB')
    while(True):
      if(filesize > 100):
        temp = copy.deepcopy(TEMPLATE)
        temp['calls'] = deck['calls'][0:100]
        temp['responses'] = deck['responses'][0:300]
        deck['calls'] = deck['calls'][100:]
        deck['responses'] = deck['responses'][300:]
        lastdeck = mergedecks(lastdeck, temp)
      if(filesize < 50):
        deck = mergedecks(deck, lastdeck)
        lastdeck = copy.deepcopy(TEMPLATE)
      filesize = (sys.getsizeof(json.dumps(deck)) - sys.getsizeof(""))/1024
      log.info('After spliting | Size: ' + str(filesize) + ' KB' + ' | Calls: ' + str(len(deck['calls'])) + ' | Responses: ' + str(len(deck['responses'])))
      if(filesize < 100):
        break
    with open(deck['name'] + '.deck.json5', 'w',encoding="utf-8") as outfile:
      json.dump(deck, outfile,ensure_ascii=False)   
import requests
import json
import math
import logging as log
import copy
import sys
from functions import *

log.basicConfig(level=log.WARN, format='%(levelname)s - %(message)s')

TEMPLATE =  {
  "name": "Name",
  "author": "Etaro",
  "calls": [],
  "responses": []}


# "calls": [[["W 2021 najnowszym bestsellerem J.K Rowling został \"Harry Potter i ", {}, "\"."]], [["Gdybym miałbyć superbohaterem, moją mocą byłoby ", {}, "."]]]
def removeblack(decks):
  for deck in decks:
    calls = deck['calls']
    for call in calls:
      blankspaces = 0
      for line in call:
        blankspaces += line.count({})
      if blankspaces > 3:
        log.info('Removing call: ' + str(call))
        deck['calls'].remove(call)
  return decks



def main():
  maindeck = copy.deepcopy(TEMPLATE)
  decksnames = []
  print('Hi there :D \nThis is a downloader of Many Decks cards, Created by Etaro \n--------------------------------------------')
  maindeck['name'] = input('Enter name of the main deck: ')
  maindeck['author'] = input('Enter author of the main deck: ')+" (Downloaded by Etaro's Many Deck Downloader))"
  print('--------------------------------------------')
  print('Enter the codes of the decks you want to download. \nWhen you are done, enter 0')
  while True:
    code = input('Enter code: ')
    if code == '0':
      break
    else:
      decksnames.append(code)
  print('--------------------------------------------')
  for deck in decksnames:
    print('Downloading deck: ' + deck)
    deck = getDeck(deck)
    if deck is not None:
      print('Deck name: ' + deck['name'])
      print('Adding deck to main deck')
      maindeck = mergedecks(maindeck, deck)
    else:
      print('Deck not found :(')
      print('Please check the code and try again')
    print('--------------------------------------------')
  print('All decks downloaded successfully!')
  print('--------------------------------------------')
  maindeck = splitdeck(maindeck)
  # if(input('Do you want to remove all black cards with more than 3 empty places? (y/n): ') == 'y'):
  #   maindeck = removeblack(maindeck)
  
  dumpdeck(maindeck)

  print('Successfully saved all decks! \nNow, you can import them to Many Decks!')
  print('Thanks for using this shitty program :D')






if __name__ == '__main__':
  main()
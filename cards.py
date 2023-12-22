#!/usr/bin/env python
# coding=utf-8

import json

# Opening JSON file
f_cards = open('./data/cards.json',)
all_cards = json.load(f_cards)  
f_cards.close()

f_deck = open('./data/deck_0.json',)
deck_json = json.load(f_deck)  
f_deck.close()

card_3_stg_atk=list(filter(lambda card : card["Name"]=="3 Stage Atk",all_cards))[0]
card_4_stg_atk=list(filter(lambda card : card["Name"]=="4 Stage Atk",all_cards))[0]
card_5_stg_atk=list(filter(lambda card : card["Name"]=="5 Stage Atk",all_cards))[0]
card_kameha=list(filter(lambda card : card["Name"]=="Kamehameha",all_cards))[0]
cards=list(filter(lambda card : card["Type"]=="Physical" or card["Type"]=="Beam" or card["Type"]=="Command" or card["Type"]=="Defense" or (card["Type"]=="Support" and "Boosts" in card.keys()) or card["Name"] in ["Resurrection","Kaio Ken","Body Change","Kibito","Champ. Belt","Sunglasses","Babidi","Rejuv Chmbr","Heart Pills","Yakon","C. C. Fridge"]
,all_cards))
cards_def=list(filter(lambda card : card["Type"]=="Defense",all_cards))

deck=[list(filter(lambda card : card["Name"]==card_name,all_cards))[0] for card_name in deck_json["cards"]]


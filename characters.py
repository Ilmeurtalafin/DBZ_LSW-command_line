#! /usr/bin/env python3
# coding=utf-8

import random 
from cards import *
import json
import numpy as np

# Opening JSON file
f_chara = open('./data/characters.json',)
characters_json = json.load(f_chara)  
f_chara.close()

class character:

	def __init__(self,chara_json={"Id": 0, "Name": "DefaultChara", "DisplayName": "CharaName", "Form Name": "Normal", "HP": 100, "Speed": 10, "Str": 10, "Ki": 10},deck_name="Damage"):
		self.id=chara_json["Id"]
		self.name=chara_json["Name"]
		self.display_name=chara_json["DisplayName"]

		self.hp_max=chara_json["HP"]
		self.hp=self.hp_max
		self.str=chara_json["Str"]
		self.ki=chara_json["Ki"]
		self.spd=chara_json["Speed"]

		self.base_stats=chara_json

		self.powered_up_counter=0
		self.guard=False
		self.position="DB"
		self.card_cost=10

		self.guard_buff=0

		self.deck=get_deck_by_name(deck_name)
		random.shuffle(self.deck)
		self.hand=[ self.deck.pop(0) for i in range(3)]
		self.limits=[card_kameha,card_5_stg_atk]
		self.limits=get_limits_by_char(self.name)

		self.kibito=False
		self.champ_belt=False
		self.sunglasses=False

		self.ai_favorite_limit=None
		limit_atk=list(filter(lambda card : "Power" in card.keys(),self.limits))
		if len(limit_atk):
			self.ai_favorite_limit=sorted(limit_atk, key=lambda card:card["Power"], reverse=True)[0]

	def get_hp_percent(self):
		return self.hp*1.0/self.hp_max

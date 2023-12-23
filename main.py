#! /usr/bin/env python3
# coding=utf-8

# TODO :
# AI
# support cards
# "hand is full"
# animations
# invading movement
# auto guard / avoiding
# cc when taking damages

import random 
from display import *
from cards import *
from characters import *
import math
import time
import json
import numpy as np
import copy



def compute_damage_position(player_off,player_def,card):
	# TODO
	damage_reduce=0
	if "B" in player_off.position:
		damage_reduce+=8
	if card["Type"]=="Beam":
		if "D" in player_off.position:
			damage_reduce+=8
	if card["Type"]=="Physical":
		if "U" in player_off.position:
			damage_reduce+=8


	return 0

def compute_damage_buff(player_off,player_def,card):
	# TODO
	return 8*player_def.guard_buff

def compute_card_damage(player_off,player_def,card):
	damage_reduce_guard=4*player_def.guard
	damage_reduce_position=compute_damage_position(player_off,player_def,card)
	damage_reduce_buff=compute_damage_buff(player_off,player_def,card)

	damage_reduce=damage_reduce_guard+damage_reduce_position+damage_reduce_buff

	damage_character=player_off.str*(card["Type"]=="physical")+player_off.ki*(card["Type"]=="beam")

	damage=card["Power"]+max(0,damage_character-damage_reduce)

	return damage


def validate_input():
	buffered=msvcrt.kbhit()

	input_string=""
	# TODO : Adapt inputs value to Linux

	char=0

	if buffered:
		# flush buffered keystrokes
		while msvcrt.kbhit():
			# read one char and get char code
			char = ord(msvcrt.getch())
	
	while True:
		# read one char and get char code
		char = ord(msvcrt.getch())

		if char == 224:
			next1 = ord(msvcrt.getch())
			if next1 == 75: # Left
				input_string="INPUT_LEFT"
				break
			elif next1 == 77: # Right
				input_string="INPUT_RIGHT"
				break
			elif next1 == 72: # Down
				input_string="INPUT_DOWN"
				break
			elif next1 == 80: # Up
				input_string="INPUT_UP"
				break
		elif char in {10, 13}:
			input_string="INPUT_ENTER"
			break
		elif char in {27,113}:
			input_string="INPUT_EXIT"
			break

	return input_string


def commands_to_symbol(commands,colors):
	symbols={"INPUT_LEFT":"<","INPUT_RIGHT":">","INPUT_UP":"v","INPUT_DOWN":"^"}
	string=""
	for i,command in enumerate(commands):
		string+=colors[i]+symbols[command]+ansi_code["Reset"]
	return string

def command_atk_display(input_sequence=["INPUT_RIGHT","INPUT_UP","INPUT_DOWN"],max_time=2.4):

	box_border=[
	color_dgrey_on_white+"█"+ansi_code["Reset"],
	color_dgrey_on_white+"█"+ansi_code["Reset"],
	color_dgrey_on_white+"█"+ansi_code["Reset"],
	color_dgrey_on_white+"█"+ansi_code["Reset"],
	color_dgrey_on_white+"█"+ansi_code["Reset"],
	color_dgrey_on_white+"█"+ansi_code["Reset"],
	color_dgrey_on_white+"█"+ansi_code["Reset"],
	color_dgrey_on_white+"█"+ansi_code["Reset"]]

	box_x=0
	box_y=TXT_BOX_Y_ORIGIN-1
	box_w=N_COL
	box_h=TXT_BOX_HEIGHT+1
	box_fill=ansi_code["BG_White"]+" "+ansi_code["Reset"]

	draw_box(box_x,box_y,box_w,box_h,box_fill,box_border)

	start_time=time.perf_counter()
	cur_time=start_time

	command_success=[False]*len(input_sequence)
	colors=[color_dgrey_on_white]*len(input_sequence)
	command_num=0
	player_inputs=[]

	# clear()
	print_custom(color_white_on_dgrey+"Push "+f'{cur_time-start_time:.1f}'+'/'+f'{max_time:.1f}',box_x+1,box_y+1)
	print_custom(commands_to_symbol(input_sequence,colors),box_x+1,box_y+3)

	while cur_time-start_time<max_time:
		if msvcrt.kbhit(): # get input
			input_string="INPUT_NONE"
			char = ord(msvcrt.getch())

			if char == 224:
				next1 = ord(msvcrt.getch())
				if next1 == 75: # Left
					input_string="INPUT_LEFT"
				elif next1 == 77: # Right
					input_string="INPUT_RIGHT"
				elif next1 == 72: # Down
					input_string="INPUT_DOWN"
				elif next1 == 80: # Up
					input_string="INPUT_UP"
			elif char in {10, 13}:
				input_string="INPUT_ENTER"
			elif char in {27,113}:
				input_string="INPUT_EXIT"

			command_success[command_num]=input_string==input_sequence[command_num]
			colors[command_num]=color_green_on_white if input_string==input_sequence[command_num] else color_red_on_white
			player_inputs+=[input_string]
			if len(player_inputs)>=len(input_sequence):
				break
			command_num+=1


		cur_time=time.perf_counter()
		# clear()
		print_custom(color_white_on_dgrey+f'{cur_time-start_time:.1f}',box_x+6,box_y+1)
		print_custom(commands_to_symbol(input_sequence,colors),box_x+1,box_y+3)

	# clear()
	print_custom(color_white_on_dgrey+"Push "+f'{cur_time-start_time:.1f}'+'/'+f'{max_time:.1f}',box_x+1,box_y+1)
	print_custom(commands_to_symbol(input_sequence,colors),box_x+1,box_y+3)

	time.sleep(1.0)

	return command_success


def command_atk(length=3,max_time=2.4):
	command_catalog=["INPUT_LEFT","INPUT_RIGHT","INPUT_UP","INPUT_DOWN"]
	input_sequence=list(random.choices(command_catalog,k=length))
	return command_atk_display(input_sequence=input_sequence,max_time=max_time)


def open_menu(items,cursor,direction="VERT",mode="MOD",position=[0,0],step_size=1,grid_size=2,refresh_disp_func=None,start_index=0):

	item_count=len(items)
	index=start_index
	input_string="INPUT_NONE"

	while not input_string=="INPUT_EXIT":
		if refresh_disp_func:
			refresh_disp_func()

		# display colored menu items + cursor 
		for i,item in enumerate(items):

			cursor_text=""
			if index==i:
				if isinstance(cursor["PreCursor ON Colors"], str):
					cursor_text+=cursor["PreCursor ON Colors"]+cursor["PreCursor ON"]
				else:
					cursor_text+=cursor["PreCursor ON Colors"][i]+cursor["PreCursor ON"]
			else :
				if isinstance(cursor["PreCursor ON Colors"], str):
					cursor_text+=cursor["PreCursor OFF Colors"]+cursor["PreCursor OFF"]
				else:
					cursor_text+=cursor["PreCursor OFF Colors"][i]+cursor["PreCursor OFF"]
			cursor_text+=ansi_code['Reset']
			
			item_text=item["item_colors"]
			item_text+=item["item_text"]
			item_text+=ansi_code["Reset"]

			post_cursor_text=""
			if index==i:
				post_cursor_text+=cursor["PostCursor ON Colors"]+cursor["PostCursor ON"]
			else :
				post_cursor_text+=cursor["PostCursor OFF Colors"]+cursor["PostCursor OFF"]
			post_cursor_text+=ansi_code['Reset']

			text=cursor_text+item_text+post_cursor_text
			
			pos_x=position[0]
			pos_y=position[1]
			if direction=="HOR":
				pos_x+=step_size*i
			elif direction=="VERT":
				pos_y+=step_size*i
			elif direction=="GRID":
				pos_x+=step_size[0]*(i//grid_size)
				pos_y+=step_size[1]*(i%grid_size)
			print_custom(text,pos_x,pos_y)

		# display current selection description 
		for descr in items[index]["item_descriptions"]:
			descr_txt=descr["text_colors"]+descr["text"]+ansi_code["Reset"]
			descr_position=descr["text_position"]
			print_custom(descr_txt,descr_position[0],descr_position[1])

		input_string=validate_input()

		if input_string=="INPUT_EXIT":
			continue

		if input_string=="INPUT_ENTER":
			if items[index]["is_valid"]:
				return input_string,index

		if direction=="HOR":
			index=index+(input_string=="INPUT_RIGHT")-(input_string=="INPUT_LEFT")
		elif direction=="VERT":
			index=index-(input_string=="INPUT_DOWN")+(input_string=="INPUT_UP")
		elif direction=="GRID":
			index=index+grid_size*((input_string=="INPUT_RIGHT")-(input_string=="INPUT_LEFT"))+(input_string=="INPUT_UP")-(input_string=="INPUT_DOWN")

		# indices[0]=indices[0]+(input_string=="INPUT_DOWN")-(input_string=="INPUT_UP")
		# indices[1]=indices[1]+(input_string=="INPUT_RIGHT")-(input_string=="INPUT_LEFT")

		if mode=="MOD":
			index=index%item_count
			# indices[0]=indices[0]%size[0]
			# indices[1]=indices[1]%size[1]
		else :
			index=max(min(index,item_count-1),0)
			# indices[0]=max(min(indices[0],size[0]-1),0)
			# indices[1]=max(min(indices[1],size[1]-1),0)

	return input_string,index



def get_hp_string(percent,max_len=32,player="p1"):

	# safety : no negative hp
	percent=max(0,percent)
	
	full_block_count=math.floor(max_len*percent)
	half_block_count=math.floor((math.floor(2*max_len*percent)-2*full_block_count))
	space_count=max_len-full_block_count-half_block_count

	# set background color to grey + set text color to green
	text=ansi_code["BG_Grey_Med"]+ansi_code["FG_Green_HP"]


	if player=="p2":
		full_block="█"
		half_block="▌"
		text+=full_block*full_block_count+half_block*half_block_count+" "*space_count
	else :
		full_block="█"
		half_block="▐"
		text+=" "*space_count+half_block*half_block_count+full_block*full_block_count

	# reset format
	text+=ansi_code["Reset"]

	return text

def print_json_img(json,origin_x=0,origin_y=0):
	for tile in json["tiles"]:
		print_custom(u"\u001b[48;5;"+str(tile["c1_index"])+"m"+u"\u001b[38;5;"+str(tile["c0_index"])+"m"+tile["char"],origin_x+tile["x"],origin_y+tile["y"])
	sys.stdout.write(ansi_code["Reset"])	
		
def refresh_txt_box():
	draw_box(0,TXT_BOX_Y_ORIGIN-1,TXT_BOX_X_ORIGIN,TXT_BOX_HEIGHT,ansi_code["BG_Grey_Dark"]+" "+ansi_code["Reset"],[ansi_code["BG_Grey_Dark"]+" "+ansi_code["Reset"]]*8)
	draw_box(TXT_BOX_X_ORIGIN,TXT_BOX_Y_ORIGIN-1,TXT_BOX_WIDTH,1,ansi_code["BG_Grey_Dark"]+" "+ansi_code["Reset"],[ansi_code["BG_Grey_Dark"]+" "+ansi_code["Reset"]]*8)
	draw_box(TXT_BOX_X_ORIGIN,TXT_BOX_Y_ORIGIN,TXT_BOX_WIDTH,TXT_BOX_HEIGHT-1,ansi_code["BG_White"]+" "+ansi_code["Reset"],[ansi_code["BG_White"]+" "+ansi_code["Reset"]]*8)
	
def print_cc(character):
	# cc display
	text=color_white_on_dgrey+"cc:"+("  "+"/"+str(character.card_cost).rjust(2,"0")).rjust(5)+ansi_code["Reset"]
	print_custom(text,N_COL-8,N_LIN-2)

def print_stage():
	# draw_box(0,BG_Y_ORIGIN,N_COL,BG_HEIGHT,ansi_code["BG_Blue_Sky"]+" "+ansi_code["Reset"],[ansi_code["BG_Blue_Sky"]+" "+ansi_code["Reset"]]*8)
	print_json_img(CUR_BACKRGOUND_JSON,0,BG_Y_ORIGIN)

def print_stage_and_txt_box():
	refresh_txt_box()
	print_stage()

def print_fight_screen():
	draw_box(0,0,N_COL,N_LIN+1,ansi_code["BG_Grey_Dark"]+" "+ansi_code["Reset"],[ansi_code["BG_Grey_Dark"]+" "+ansi_code["Reset"]]*8)
	print_stage()
	# print_custom(color_white_on_dgrey+"VS"+ansi_code["Reset"],N_COL//2-1,2)
	print_json_img(vs_json,(N_COL-16)//2,0)
	refresh_txt_box()

def print_hp_bars(hp1=0.85,hp2=0.85):
	text1=get_hp_string(hp1,HP_BAR_LEN,"p1")
	text2=get_hp_string(hp2,HP_BAR_LEN,"p2")
	print_custom(text1,HP_X_MARGIN,HP_Y)
	print_custom(text2,N_COL-HP_BAR_LEN-HP_X_MARGIN,HP_Y)

def print_atk_def(turn_type):
	pos_p1_x=HP_X_MARGIN+HP_BAR_LEN-7
	pos_p2_x=N_COL-(HP_X_MARGIN+HP_BAR_LEN)
	txt_p1,txt_p2 = (color_dgrey_on_green+"ATTACK ",color_dgrey_on_mgrey+"DEFENSE") if turn_type=="ATK" else (color_dgrey_on_mgrey+"DEFENSE",color_dgrey_on_green+"ATTACK ")
	print_custom(txt_p1,pos_p1_x,HP_Y+1)
	print_custom(txt_p2,pos_p2_x,HP_Y+1)


def print_sprites(characters):
	match characters[0].position:
		case "UB":
			pos_x=CHARACTER_POS_ORIGIN[0]
			pos_y=CHARACTER_POS_ORIGIN[1]
		case "DB":
			pos_x=CHARACTER_POS_ORIGIN[0]
			pos_y=CHARACTER_POS_ORIGIN[1]+CHARACTER_POS_STEPS[1]
		case "UF":
			pos_x=CHARACTER_POS_ORIGIN[0]+CHARACTER_POS_STEPS[0]
			pos_y=CHARACTER_POS_ORIGIN[1]
		case "DF":
			pos_x=CHARACTER_POS_ORIGIN[0]+CHARACTER_POS_STEPS[0]
			pos_y=CHARACTER_POS_ORIGIN[1]+CHARACTER_POS_STEPS[1]
	print_custom(ansi_code["BG_Orange"]+" "+ansi_code["Reset"],pos_x,pos_y)
	print_json_img(json.load(open('./data/sprite_goku.json')),pos_x,pos_y)

	match characters[1].position:
		case "UB":
			pos_x=N_COL-(CHARACTER_POS_ORIGIN[0])
			pos_y=CHARACTER_POS_ORIGIN[1]
		case "DB":
			pos_x=N_COL-(CHARACTER_POS_ORIGIN[0])
			pos_y=CHARACTER_POS_ORIGIN[1]+CHARACTER_POS_STEPS[1]
		case "UF":
			pos_x=N_COL-(CHARACTER_POS_ORIGIN[0]+CHARACTER_POS_STEPS[0])
			pos_y=CHARACTER_POS_ORIGIN[1]
		case "DF":
			pos_x=N_COL-(CHARACTER_POS_ORIGIN[0]+CHARACTER_POS_STEPS[0])
			pos_y=CHARACTER_POS_ORIGIN[1]+CHARACTER_POS_STEPS[1]
	print_custom(ansi_code["BG_Blue"]+" "+ansi_code["Reset"],pos_x,pos_y)
	print_json_img(json.load(open('./data/sprite_vegeta.json')),pos_x,pos_y)



def print_HUD(characters):
	print_hp_bars(characters[0].get_hp_percent(),characters[1].get_hp_percent())

	#  print speed *
	pos_p1_x=HP_X_MARGIN+HP_BAR_LEN-9
	pos_p2_x=N_COL-(HP_X_MARGIN+HP_BAR_LEN)+8
	txt_p1,txt_p2 = (color_white_on_dgrey+"*"+ansi_code["Reset"],color_white_on_dgrey+" "+ansi_code["Reset"]) if characters[0].spd>=characters[1].spd else (color_white_on_dgrey+" "+ansi_code["Reset"],color_white_on_dgrey+"*"+ansi_code["Reset"])
	print_custom(txt_p1,pos_p1_x,HP_Y+1)
	print_custom(txt_p2,pos_p2_x,HP_Y+1)

	

	# print names
	print_custom(color_white_on_dgrey+characters[0].display_name+ansi_code["Reset"],HP_X_MARGIN,HP_Y-1)
	print_custom(color_white_on_dgrey+characters[1].display_name+ansi_code["Reset"],N_COL-len(characters[1].display_name)-HP_X_MARGIN,HP_Y-1)

	# print_stage()

	print_cc(characters[0])



def print_debug(characters):
	pos_p1_x=HP_X_MARGIN+HP_BAR_LEN-9
	pos_p2_x=pos_p1_x+15

	pos_y=BG_Y_ORIGIN+1

	sys.stdout.write(color_white_on_dgrey)
	
	off_y=0
	print_custom("HP : "+str(characters[0].hp)+"/"+str(characters[0].hp_max),pos_p1_x,pos_y+off_y)
	print_custom("HP : "+str(characters[1].hp)+"/"+str(characters[1].hp_max),pos_p2_x,pos_y+off_y)
	off_y+=1
	print_custom("STR: "+str(characters[0].str),pos_p1_x,pos_y+off_y)
	print_custom("STR: "+str(characters[1].str),pos_p2_x,pos_y+off_y)
	off_y+=1
	print_custom("SPD: "+str(characters[0].spd),pos_p1_x,pos_y+off_y)
	print_custom("SPD: "+str(characters[1].spd),pos_p2_x,pos_y+off_y)
	off_y+=1
	print_custom("KI : "+str(characters[0].ki),pos_p1_x,pos_y+off_y)
	print_custom("KI : "+str(characters[1].ki),pos_p2_x,pos_y+off_y)
	off_y+=1
	print_custom("GB : "+str(characters[0].guard_buff),pos_p1_x,pos_y+off_y)
	print_custom("GB : "+str(characters[1].guard_buff),pos_p2_x,pos_y+off_y)
	off_y+=1
	print_custom("CC : "+str(characters[0].card_cost),pos_p1_x,pos_y+off_y)
	print_custom("CC : "+str(characters[1].card_cost),pos_p2_x,pos_y+off_y)



def print_action(action_descr,delay):
	# box_border=[color_dgrey_on_white+"█"+ansi_code["Reset"]]*8

	box_border=[
	color_dgrey_on_white+"█"+ansi_code["Reset"],
	color_dgrey_on_white+"█"+ansi_code["Reset"],
	color_dgrey_on_white+"█"+ansi_code["Reset"],
	color_dgrey_on_white+"█"+ansi_code["Reset"],
	color_dgrey_on_white+"█"+ansi_code["Reset"],
	color_dgrey_on_white+"█"+ansi_code["Reset"],
	color_dgrey_on_white+"█"+ansi_code["Reset"],
	color_dgrey_on_white+"█"+ansi_code["Reset"]]

	box_x=0
	box_y=TXT_BOX_Y_ORIGIN-1
	box_w=N_COL
	box_h=TXT_BOX_HEIGHT+1
	box_fill=ansi_code["BG_White"]+" "+ansi_code["Reset"]

	draw_box(box_x,box_y,box_w,box_h,box_fill,box_border)
	print_custom(color_dgrey_on_white,box_x+2,box_y+2)
	print_custom(action_descr,box_x+2,box_y+2)
	print_custom(ansi_code["Reset"],box_x+2,box_y+2)
	time.sleep(delay)

	print_custom(ansi_code["BG_Grey_Dark"]+" "*N_COL+ansi_code["Reset"],0,N_LIN-2)


def support_card(character,opponent,card,turn_type):
	boosts={"Speed":"spd","Str":"str","Ki":"ki","Guard":"guard_buff"}
	if "Boosts" in card.keys():
		for key in boosts.keys():
			if key in card["Boosts"].keys():
				boost=card["Boosts"][key]
				target=character if boost>0 else opponent
				cur_value=getattr(target,boosts[key])
				setattr(target,boosts[key],cur_value+boost)

		character.guard_buff=min(max(-3,character.guard_buff),+3)
		opponent.guard_buff=min(max(-3,opponent.guard_buff),+3)
		opponent.str=max(0,opponent.str)
		opponent.spd=max(0,opponent.spd)
		opponent.ki=max(0,opponent.ki)

	if card["Name"]=="Resurrection":
		card_max_gain=0
		if turn_type=="ATK":
			card_max_gain=character.hp_max//4
		else :
			card_max_gain=character.hp_max//2
		hp_gain=min(character.hp_max-character.hp,card_max_gain)
		for i in range(hp_gain):
			character.hp+=1
			print_HUD(character)
			time.sleep(0.01)

	if card["Name"]=="Kaio Ken":
		character.str*=2
		character.ki*=2

	if card["Name"]=="Body Change": # TODO "unblockable"
		opponent.hp=opponent.hp//2

	if card["Name"]=="Kibito":
		character.kibito=True

	if card["Name"]=="Champ. Belt":
		character.champ_belt=True

	if card["Name"]=="Sunglasses":
		character.sunglasses=True

	if card["Name"]=="Babidi":
		opponent.str=min(opponent.str,opponent.base_stats["Str"])
		opponent.spd=min(opponent.spd,opponent.base_stats["Speed"])
		opponent.ki=min(opponent.ki,opponent.base_stats["Ki"])

	if card["Name"]=="Rejuv Chmbr" or card["Name"]=="Heart Pills":
		character.str=max(character.str,character.base_stats["Str"])
		character.spd=max(character.spd,character.base_stats["Speed"])
		character.ki=max(character.ki,character.base_stats["Ki"])


	if card["Name"]=="Yakon":
		if opponent.powered_up_counter!=0: # if gather up activated, cancel buffs
			opponent.str-=4 
			opponent.ki-=4 
		opponent.powered_up_counter=0

	if card["Name"]=="C. C. Fridge":
		character.card_cost+=5
	

	# todo

	## sure hit
	# lockon 
	# Reading Ki
	# Feint

	# Afterimage increase block/auto avoid chance

	## knock ennemy down / reduce damage
	# tien
	# yajirobe
	# hercule
	# dabura 

	# Gamebomb
	# Spcl. Candy

	## heal amount
	# dende
	# Medical Mach

	# Qwk-Stop Dvc killandroid

	# Hourglass what are support icons?
	# Roshi’s book how are damage computed?




def is_fight_over(characters):
	if characters[0].hp>0 and characters[1].hp>0:
		return False
	else:
		return True

def get_menu_items_from_card_list(character,card_list,turn_type,default_valid=True):
	menu_items=[]
	for card in card_list:
		item_text=card["Type"][0]
		isvalid_cost=True
		if "Cost" in  card.keys():
			isvalid_cost=character.card_cost>=card["Cost"]
		isvalid_turn=True
		if turn_type=="ATK":
			if card["Type"]=="Defense":
				isvalid_turn=False
		if turn_type=="DEF":
			if card["Type"]=="Beam" or card["Type"]=="Physical" or card["Type"]=="Command":
				isvalid_turn=False

		isvalid=isvalid_turn and isvalid_cost and default_valid
		item_color=[color_mgrey_on_dgrey,color_white_on_dgrey][isvalid]
		item_descr_txt=card["Name"]
		item_descr_txt+=u"\u001b[1B"#down 1 line
		item_descr_txt+=u"\u001b["+str(len(card["Name"]))+"D"#back to start of line
		if card["Type"]=="Beam":
			item_descr_txt+="Pow. "+str(card["Power"])+"/"+"Beam"
		elif card["Type"]=="Physical":
			item_descr_txt+="Pow. "+str(card["Power"])+"/"+"Damg"
		elif card["Type"]=="Command":
			item_descr_txt+="Pow. --/"+"Comm"
		elif "Descr" in card.keys():
			item_descr_txt+=card["Descr"]
			
		menu_items+=[{"item_text":item_text,"item_colors":item_color,"is_valid":isvalid,"item_descriptions":[{"text":item_descr_txt,"text_colors":color_dgrey_on_white,"text_position":[TXT_BOX_X_ORIGIN,TXT_BOX_Y_ORIGIN+1]},
																							  {"text":str(card["Cost"]).rjust(2,"0"),"text_colors":item_color,"text_position":[N_COL-5,N_LIN-2]}]}]
	return menu_items


def start_fight():
	# clear()


	# random_character0=np.random.choice(characters_json,1)[0]
	random_character0=list(filter(lambda chara : chara["Name"]=="Goku",characters_json))[0]
	random_form0=np.random.choice(random_character0["Forms"],1)[0]
	player0_chara = {k: v for k, v in random_character0.items() if k!="Forms"}|{k: v for k, v in random_form0.items()}

	# random_character1=np.random.choice(characters_json,1)[0]
	random_character1=list(filter(lambda chara : chara["Name"]=="Vegeta",characters_json))[0]
	random_form1=np.random.choice(random_character1["Forms"],1)[0]
	player1_chara = {k: v for k, v in random_character1.items() if k!="Forms"}|{k: v for k, v in random_form1.items()}

	characters=[character(player0_chara,deck_name="Damage"),character(player1_chara,deck_name="Vegeta")]

	# orange battle screen
	print_json_img(battle_screen_json,0,0)
	# print names
	print_custom(color_white_on_dgrey+characters[0].display_name+ansi_code["Reset"],CHARACTER_NAME_POS_X,CHARACTER_NAME_POS_Y)
	print_custom(color_white_on_dgrey+characters[1].display_name+ansi_code["Reset"],N_COL-len(characters[1].display_name)-CHARACTER_NAME_POS_X,CHARACTER_NAME_POS_Y)
	time.sleep(1.0)
	# input()


	mode="LIM"
	direction="HOR"
	step_size=4
	position=[TXT_BOX_X_ORIGIN-1,TXT_BOX_Y_ORIGIN-1]

	menu_items={"ATK":items_fight_off,"DEF":items_fight_def}
	turn_num=0
	turn_types=["ATK","DEF"] if characters[0].spd>=characters[1].spd else ["DEF","ATK"]

	# update CC
	if turn_types[turn_num%2]=="DEF":
		characters[1].card_cost+=3
	else:
		characters[0].card_cost+=3

	# draw a card
	if turn_types[turn_num%2]=="ATK" and len(characters[0].hand)<6:
		characters[0].hand+=list(np.random.choice(characters[0].deck, 1))

	input_string="INPUT_NONE"
	index=0

	player_action=None
	ai_action=None



	print_fight_screen()
	print_HUD(characters)
	print_sprites(characters)

	for i in range(101):
		print_hp_bars(i/100,i/100)
		time.sleep(0.01)

	print_atk_def(turn_types[turn_num%2])


	while (not is_fight_over(characters)) and input_string!="INPUT_EXIT":

		print_HUD(characters)
		print_sprites(characters)
		print_atk_def(turn_types[turn_num%2])
		# print_debug(characters)
		
		# choose atk/def turn menu
		cur_menu_items=menu_items[turn_types[turn_num%2]]
		
		# wait for player choice
		input_string,index=open_menu(cur_menu_items,cursor_fight,direction=direction,mode=mode,position=position,step_size=step_size,refresh_disp_func=refresh_txt_box,start_index=index)
		
		if input_string=="INPUT_EXIT":
			continue

		# deeper level menus
		if index==0: # Limit Action menu
			items=get_menu_items_from_card_list(characters[0],characters[0].limits,turn_types[turn_num%2],characters[0].powered_up_counter>0)
			input_string_2,index_2=open_menu(items,cursor_fight,direction=direction,mode=mode,position=position,step_size=step_size,refresh_disp_func=refresh_txt_box)
			
			if input_string_2=="INPUT_EXIT":
				continue

			if characters[0].card_cost<characters[0].limits[index_2]["Cost"]:
				continue

			player_action={"type":"card","card":copy.deepcopy(characters[0].limits[index_2])}
		
		if index==1: # Joint Action menu
			items=get_menu_items_from_card_list(characters[0],characters[0].hand,turn_types[turn_num%2])
			input_string_2,index_2=open_menu(items,cursor_fight,direction=direction,mode=mode,position=position,step_size=step_size,refresh_disp_func=refresh_txt_box)
			
			if input_string_2=="INPUT_EXIT":
				continue

			player_action={"type":"card","card":copy.deepcopy(characters[0].hand[index_2]),"index":index_2}
		
		if index==2: # Basic Action Menu
			if turn_types[turn_num%2]=="ATK":
				# choose basic action based on powered up state
				items=items_basic_off[characters[0].powered_up_counter>0]
				
				input_string_2,index_2=open_menu(items,cursor_fight,direction=direction,mode=mode,position=position,step_size=step_size,refresh_disp_func=refresh_txt_box)
				
				if input_string_2=="INPUT_EXIT":
					continue
				
				if index_2==0: # 3/4 stg attack card
					player_action={"type":"card","card":copy.deepcopy([card_3_stg_atk,card_4_stg_atk][characters[0].powered_up_counter>0])}

				if index_2==1:
					player_action={"type":"gather_power"}

			elif turn_types[turn_num%2]=="DEF":

				input_string_2="INPUT_NONE"
				index_2=0
				player_action=None
				
				# basic action def menu, while loop added to handle movement submenu 
				while input_string_2!="INPUT_EXIT":
					
					print_HUD(characters)
					print_atk_def(turn_types[turn_num%2])

					input_string_2,index_2=open_menu(items_basic_def,cursor_fight,direction=direction,mode=mode,position=position,step_size=step_size,refresh_disp_func=refresh_txt_box)
					
					if input_string_2=="INPUT_EXIT":
						continue

					if index_2==0:
						player_action={"type":"guard"}
						input_string_2="INPUT_EXIT"
						continue

					if index_2==1:

						positions=["UB","DB","UF","DF"]
						cur_pos_index=positions.index(characters[0].position)

						grid_size=2

						for i in range(len(items_movement)):
							items_movement[i]["is_valid"]=(cur_pos_index!=i)

							# update move cursor color based on background tile color
							px=MOVE_ARROW_ORIGIN[0]+MOVE_ARROW_STEPS[0]*(i//grid_size)
							py=MOVE_ARROW_ORIGIN[1]+MOVE_ARROW_STEPS[1]*(i%grid_size)-BG_Y_ORIGIN
							color_index=list(filter(lambda tile : tile["x"]==px and tile["y"]==py,CUR_BACKRGOUND_JSON["tiles"]))[0]["c0_index"]
							cursor_move["PreCursor ON Colors"][i]=u"\u001b[48;5;"+str(color_index)+"m"+ansi_code["FG_Yellow"]
							cursor_move["PreCursor OFF Colors"][i]=u"\u001b[48;5;"+str(color_index)+"m"+ansi_code["FG_Yellow"]

						input_string_3,index_3=open_menu(items_movement,cursor_move,direction="GRID",grid_size=grid_size,mode=mode,position=MOVE_ARROW_ORIGIN,step_size=MOVE_ARROW_STEPS,refresh_disp_func=refresh_txt_box,start_index=cur_pos_index)
						print_stage()
						print_sprites(characters)

						if input_string_3=="INPUT_EXIT":
							continue

						player_action={"type":"movement","new_position":positions[index_3]}
						input_string_2="INPUT_EXIT"
						continue

				if player_action:
					pass
				elif input_string_2=="INPUT_EXIT":
					continue

		if index==3:
			continue
			player_action={"type":"character"}

		if len(characters[0].hand)==6 and player_action["type"]=="card":
			if "index" in player_action.keys():
				# todo "hand is full"
				pass


		# TODO
		# get AI action
		# tmp guard/3stg atk
		ai_action=None
		if turn_types[turn_num%2]=="ATK":#atk for player, so ai in def
			ai_action={"type":"guard"}
		else :

			if characters[1].powered_up_counter>0: 
				# most powerful limit
				card=characters[1].ai_favorite_limit
				if card is not None:
					if card["Type"]=="Beam" or card["Type"]=="Physical" or card["Type"]=="Command":
						if characters[1].card_cost>card["Cost"]:
							ai_action={"type":"card","card":card}

				# other limits
				for i in range(len(characters[1].limits)):
					if ai_action==None:
						card=characters[1].limits[i]
						if card["Type"]=="Beam" or card["Type"]=="Physical" or card["Type"]=="Command":
							if characters[1].card_cost>card["Cost"]:
								ai_action={"type":"card","card":card}
			
			if ai_action==None:
				# Gather power
				if characters[1].powered_up_counter==0:
					if characters[1].ai_favorite_limit is not None:
						if characters[1].card_cost>=characters[1].ai_favorite_limit["Cost"]-8:
							ai_action={"type":"gather_power"}
					elif characters[1].card_cost>=15:
						ai_action={"type":"gather_power"}

			if ai_action==None:
				for i in range(len(characters[1].hand)):
					card=characters[1].hand[i]
					if card["Type"]=="Beam" or card["Type"]=="Physical" or card["Type"]=="Command":
						if characters[1].card_cost>card["Cost"]:
							if ai_action==None or  card["Power"]>ai_action["card"]["Power"]:
								ai_action={"type":"card","card":card,"index":i}

			# Basic command atk
			if ai_action==None:
				ai_action={"type":"card","card":[card_3_stg_atk,card_4_stg_atk][characters[1].powered_up_counter>0]}
			
			


		# apply action
		character_atk,character_def = (characters[0],characters[1]) if turn_types[turn_num%2]=="ATK" else (characters[1],characters[0])
		action_atk,action_def = (player_action,ai_action) if turn_types[turn_num%2]=="ATK" else (ai_action,player_action)

		atk_action_descr=[character_atk.name+"'s attack :",""]
		def_action_descr=[character_def.name+"'s guard :",""]

		# get action strings and display them
		match action_def["type"]:
			case "guard":
				def_action_descr[1]="Squared off"
			case "movement":
				def_action_descr[1]="Movement"
			# TODO handle support cards
			case "card":
				def_action_descr[1]=action_def["card"]["Name"]

		is_command_atk=False
		match action_atk["type"]:
			case "gather_power":
				atk_action_descr[1]="Gather power"
			case "card":
				atk_action_descr[1]=action_atk["card"]["Name"]
				if action_atk["card"]["Type"]=="Command" and turn_types[turn_num%2]=="ATK":
					is_command_atk=True

		print_json_img(CUR_ACTION_BACKRGOUND_JSON,0,BG_Y_ORIGIN)
		print_action(atk_action_descr,1)
		if is_command_atk:
			command_success=command_atk(length=action_atk["card"]["max_cc"],max_time=2.4)
			counter=0
			for command in command_success:
				if command:
					counter+=1
				else :
					break
			action_atk["card"]["max_cc"]=counter
			action_atk["card"]["Power"]=counter/2.0


		print_action(def_action_descr,1)

		
		
		
		# update characters
		match action_def["type"]:
			case "guard":
				character_def.guard=True
			case "movement":
				character_def.position=action_def["new_position"]
			case "card":
				character_def.card_cost-=action_def["card"]["Cost"]

				# TODO func handling support cards
				if action_def["card"]["Type"]=="Support":
					support_card(character_def,character_atk,action_def["card"],turn_types[turn_num%2])

				# if card if from hand, remove it
				if "index" in action_def.keys():
					del character_def.hand[action_def["index"]]

		match action_atk["type"]:
			case "gather_power":
				if character_atk.powered_up_counter==0: # add gathered power buffs only if not already in gathered state
					character_atk.str+=4 
					character_atk.ki+=4 
				character_atk.powered_up_counter=3
			case "card":
				computed_damage=0

				if "Power" in action_atk["card"].keys():
					computed_damage=compute_card_damage(character_atk,character_def,action_atk["card"])

				damage_coef=1.0

				if action_def["type"]=="card":
					if action_def["card"]["Type"]=="Defense":
						# damage cancelled/avoided
						if action_def["card"]["Def_type"]==action_atk["card"]["Type"]:
							if action_def["card"]["Name"]=="Taiyoken" and character_atk.sunglasses:
								pass
							else :
								damage_coef=0.0
						# damage endured
						elif action_def["card"]["Name"]=="Endurance":
							computed_damage=action_atk["card"]["Cost"]

				if action_atk["card"]["Type"]=="Beam" and character_def.kibito:
					damage_coef=0.0
					character_def.kibito=False

				if action_atk["card"]["Type"]=="Physical" and character_def.champ_belt:
					damage_coef=0.0
					character_def.champ_belt=False

				if action_atk["card"]["Type"]=="Command":
					# TODO command inputs
					character_atk.card_cost+=action_atk["card"]["max_cc"]
				elif action_atk["card"]["Type"]=="Support":
					support_card(character_atk,character_def,action_atk["card"],turn_types[turn_num%2])
				
				character_atk.card_cost-=action_atk["card"]["Cost"]

				final_damage=int(computed_damage*damage_coef)
				for i in range(final_damage):
					character_def.hp-=1
					print_HUD(characters)
					time.sleep(0.01)

				if action_atk["card"]["Name"]=="Ki Absorber":
					for i in range(final_damage):
						character_atk.hp+=1
						print_HUD(characters)
						time.sleep(0.01)


				if "index" in action_atk.keys():
					del character_atk.hand[action_atk["index"]]



		# prepare next turn
		turn_num+=1

		if turn_num%2==0:
			turn_types=["ATK","DEF"] if characters[0].spd>=characters[1].spd else ["DEF","ATK"]


		index=0

		if turn_types[turn_num%2]=="ATK" and characters[0].powered_up_counter>0:
			characters[0].powered_up_counter-=1
			if characters[0].powered_up_counter==0: # cancel gathered power buffs
				characters[0].str-=4 
				characters[0].ki-=4 
		if turn_types[turn_num%2]=="DEF" and characters[1].powered_up_counter>0:
			characters[1].powered_up_counter-=1
			if characters[1].powered_up_counter==0: # cancel gathered power buffs
				characters[1].str-=4 
				characters[1].ki-=4 

		characters[0].guard=False
		characters[1].guard=False

		# update CC
		if turn_types[turn_num%2]=="DEF":
			characters[1].card_cost+=3
		else:
			characters[0].card_cost+=3

		# draw a card
		if turn_types[turn_num%2]=="ATK" and len(characters[0].hand)<6 and len(characters[0].deck)>0:
			characters[0].hand+=[characters[0].deck.pop(0)]
		if turn_types[turn_num%2]=="DEF" and len(characters[1].hand)<6 and len(characters[1].deck)>0:
			characters[1].hand+=[characters[1].deck.pop(0)]


		# update HUD
		print_stage()
		print_HUD(characters)
		print_atk_def(turn_types[turn_num%2])


		


def exit_game():
	# clear console and restore cursor before exit
	print(ansi_code["Reset"])
	clear()
	show_cursor()

def title_screen():
	# display "press enter" menu

	print_json_img(title_screen_json,0,0)

	sys.stdout.write(ansi_code["Reset"])

	press_enter_txt="Press enter"
	print_custom(color_dgrey_on_white+press_enter_txt,(N_COL-len(press_enter_txt))//2,23)
	sys.stdout.write(ansi_code["Reset"])

	# loop waiting for enter key
	while True:
		# read one char and get char code
		char = ord(msvcrt.getch())

		if char in {10, 13}:
			start_fight()
			exit_game()
			break	
		elif char in {27,113}:
			exit_game()
			break


def init_game():
	title_screen()


init_console()

# for card in deck:
# 	print(card)
# input()

init_game()

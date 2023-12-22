#!/usr/bin/env python
# coding=utf-8

import os, sys
import msvcrt
from ansi_codes import *
import json

# resize the console
N_COL=80
N_LIN=37

# Fight screen constants
HP_BAR_LEN=30
HP_Y=3
HP_X_MARGIN=4

BG_Y_ORIGIN=6
BG_HEIGHT=20

TXT_BOX_X_ORIGIN=26
TXT_BOX_Y_ORIGIN=27
TXT_BOX_WIDTH=min(N_COL-TXT_BOX_X_ORIGIN+1,N_COL)
TXT_BOX_HEIGHT=9

CHARACTER_POS_ORIGIN=[N_COL//5,11]
CHARACTER_POS_STEPS=[N_COL//5,9]

MOVE_ARROW_ORIGIN=[N_COL//5+2,10]
MOVE_ARROW_STEPS=CHARACTER_POS_STEPS

# Orange battle screen constants
CHARACTER_NAME_POS_X = 12
CHARACTER_NAME_POS_Y = 17



### COLORS ###

color_white_on_dgrey=ansi_code["FG_White"]+ansi_code["BG_Grey_Dark"]
color_mgrey_on_dgrey=ansi_code["FG_Grey_Med"]+ansi_code["BG_Grey_Dark"]
color_dgrey_on_white=ansi_code["FG_Grey_Dark"]+ansi_code["BG_White"]
color_mgrey_on_white=ansi_code["FG_Grey_Med"]+ansi_code["BG_White"]
color_dgrey_on_mgrey=ansi_code["FG_Grey_Dark"]+ansi_code["BG_Grey_Med"]

color_dgrey_on_green=ansi_code["FG_Grey_Dark"]+ansi_code["BG_Green_HP"]
color_green_on_white=ansi_code["FG_Green_HP"]+ansi_code["BG_White"]
color_red_on_white=ansi_code["Red"]+ansi_code["BG_White"]
color_green_on_dgrey=ansi_code["FG_Green_HP"]+ansi_code["BG_Grey_Dark"]
color_yellow_on_dgrey=ansi_code["FG_Yellow"]+ansi_code["BG_Blue_Sky"]



### MENUS ###

items_fight_off=[
{"item_text":"L","item_colors":color_white_on_dgrey,"is_valid":True,"item_descriptions":[{"text":"Sel. limited   ","text_colors":color_dgrey_on_white,"text_position":[TXT_BOX_X_ORIGIN,TXT_BOX_Y_ORIGIN+1]}]},
{"item_text":"J","item_colors":color_white_on_dgrey,"is_valid":True,"item_descriptions":[{"text":"Sel. a card    ","text_colors":color_dgrey_on_white,"text_position":[TXT_BOX_X_ORIGIN,TXT_BOX_Y_ORIGIN+1]}]},
{"item_text":"B","item_colors":color_white_on_dgrey,"is_valid":True,"item_descriptions":[{"text":"Sel. basic     ","text_colors":color_dgrey_on_white,"text_position":[TXT_BOX_X_ORIGIN,TXT_BOX_Y_ORIGIN+1]}]},
{"item_text":"C","item_colors":color_mgrey_on_dgrey,"is_valid":False,"item_descriptions":[{"text":"Sel. chara.    ","text_colors":color_dgrey_on_white,"text_position":[TXT_BOX_X_ORIGIN,TXT_BOX_Y_ORIGIN+1]}]}
]

items_fight_def=[
{"item_text":"L","item_colors":color_white_on_dgrey,"is_valid":True,"item_descriptions":[{"text":"Sel. limited   ","text_colors":color_dgrey_on_white,"text_position":[TXT_BOX_X_ORIGIN,TXT_BOX_Y_ORIGIN+1]}]},
{"item_text":"J","item_colors":color_white_on_dgrey,"is_valid":True,"item_descriptions":[{"text":"Sel. a card    ","text_colors":color_dgrey_on_white,"text_position":[TXT_BOX_X_ORIGIN,TXT_BOX_Y_ORIGIN+1]}]},
{"item_text":"B","item_colors":color_white_on_dgrey,"is_valid":True,"item_descriptions":[{"text":"Sel. basic     ","text_colors":color_dgrey_on_white,"text_position":[TXT_BOX_X_ORIGIN,TXT_BOX_Y_ORIGIN+1]}]},
]


items_basic_def=[
{"item_text":"G","item_colors":color_white_on_dgrey,"is_valid":True,"item_descriptions":[{"text":"Guard          ","text_colors":color_dgrey_on_white,"text_position":[TXT_BOX_X_ORIGIN,TXT_BOX_Y_ORIGIN+1]}]},
{"item_text":"M","item_colors":color_white_on_dgrey,"is_valid":True,"item_descriptions":[{"text":"Movement       ","text_colors":color_dgrey_on_white,"text_position":[TXT_BOX_X_ORIGIN,TXT_BOX_Y_ORIGIN+1]}]}
]

items_basic_off={
False:[
{"item_text":"3","item_colors":color_white_on_dgrey,"is_valid":True,"item_descriptions":[{"text":"3 Stage Atk.   ","text_colors":color_dgrey_on_white,"text_position":[TXT_BOX_X_ORIGIN,TXT_BOX_Y_ORIGIN+1]}]},
{"item_text":"P","item_colors":color_white_on_dgrey,"is_valid":True,"item_descriptions":[{"text":"Gather Power   ","text_colors":color_dgrey_on_white,"text_position":[TXT_BOX_X_ORIGIN,TXT_BOX_Y_ORIGIN+1]}]}
],
True:[
{"item_text":"4","item_colors":color_white_on_dgrey,"is_valid":True,"item_descriptions":[{"text":"4 Stage Atk.   ","text_colors":color_dgrey_on_white,"text_position":[TXT_BOX_X_ORIGIN,TXT_BOX_Y_ORIGIN+1]}]},
{"item_text":"P","item_colors":color_white_on_dgrey,"is_valid":True,"item_descriptions":[{"text":"Gather Power   ","text_colors":color_dgrey_on_white,"text_position":[TXT_BOX_X_ORIGIN,TXT_BOX_Y_ORIGIN+1]}]}
]
}

items_movement=[
{"item_text":"","item_colors":color_white_on_dgrey,"is_valid":True,"item_descriptions":[{"text":"Guard Up + Damg Guard","text_colors":color_dgrey_on_white,"text_position":[TXT_BOX_X_ORIGIN,TXT_BOX_Y_ORIGIN+1]}]},
{"item_text":"","item_colors":color_white_on_dgrey,"is_valid":True,"item_descriptions":[{"text":"Guard Up + Beam Guard","text_colors":color_dgrey_on_white,"text_position":[TXT_BOX_X_ORIGIN,TXT_BOX_Y_ORIGIN+1]}]},
{"item_text":"","item_colors":color_white_on_dgrey,"is_valid":True,"item_descriptions":[{"text":"Attack Up + Damg Guard","text_colors":color_dgrey_on_white,"text_position":[TXT_BOX_X_ORIGIN,TXT_BOX_Y_ORIGIN+1]}]},
{"item_text":"","item_colors":color_white_on_dgrey,"is_valid":True,"item_descriptions":[{"text":"Attack Up + Beam Guard","text_colors":color_dgrey_on_white,"text_position":[TXT_BOX_X_ORIGIN,TXT_BOX_Y_ORIGIN+1]}]}
]


### CURSORS ###

cursor_fight={
"PreCursor ON":"►",
"PreCursor OFF":" ",
"PreCursor ON Colors":color_green_on_dgrey,
"PreCursor OFF Colors":color_white_on_dgrey,
"PostCursor ON":" ",
"PostCursor OFF":" ",
"PostCursor ON Colors":color_white_on_dgrey,
"PostCursor OFF Colors":color_white_on_dgrey
}

cursor_move={
"PreCursor ON":"▼",
"PreCursor OFF":" ",
"PreCursor ON Colors":[color_yellow_on_dgrey]*4,
"PreCursor OFF Colors":[color_yellow_on_dgrey]*4,
"PostCursor ON":"",
"PostCursor OFF":"",
"PostCursor ON Colors":color_yellow_on_dgrey,
"PostCursor OFF Colors":color_yellow_on_dgrey
}

### screen json ###

# Opening JSON file
title_screen_file = open('./data/title_screen.json')
title_screen_json = json.load(title_screen_file)  
title_screen_file.close()

battle_screen_file = open('./data/battle_screen.json')
battle_screen_json = json.load(battle_screen_file)  
battle_screen_file.close()

vs_file = open('./data/vs.json')
vs_json = json.load(vs_file)  
vs_file.close()

bg0_file = open('./data/backgrounds/bg12.json')
bg0_json = json.load(bg0_file)  
bg0_file.close()

bg0a_file = open('./data/backgrounds/bg0a.json')
bg0a_json = json.load(bg0a_file)  
bg0a_file.close()

CUR_BACKRGOUND_JSON=bg0_json
CUR_ACTION_BACKRGOUND_JSON=bg0a_json

#-----#

no_borders=[" "]*8
default_borders=["X","-","X","|","|","X","-","X"]
extended_borders=["╔","═","╗","║","║","╚","═","╝"]


def hide_cursor():
	print('\033[?25l', end="")

def show_cursor():
	print('\033[?25h', end="")


#clear the console
def clear():
	# clear console content
	print(ansi_code["Clear Console"]) 

	# go back to 0,0
	sys.stdout.write(u"\u001b["+str(N_COL)+"D")
	sys.stdout.write(u"\u001b["+str(N_LIN)+"A")	

def print_center(text):
	n_space=N_COL-len(text)
	n_space_0=int(n_space/2)
	n_space_1=n_space-n_space_0
	print(n_space_0*" "+text+n_space_1*" ")

def print_custom(text,x,y):
	if isinstance(text, str):
		# go back to 0,0
		sys.stdout.write(u"\u001b["+str(N_COL)+"D")
		sys.stdout.write(u"\u001b["+str(N_LIN)+"A")

		# go to line "y"
		if y>0:
			sys.stdout.write(u"\u001b["+str(y)+"B")

		# go to column "x"
		if x>0:
			sys.stdout.write(u"\u001b["+str(x)+"C")

		# write text
		sys.stdout.write(text)
		sys.stdout.flush()
	else :
		# if text is an array (text on multiple lines) print_custom each line under the precedent
		for i,line in enumerate(text):
			print_custom(line,x,y+i)



def draw_box(x,y,w,h,fill_character="",borders=default_borders):
	#go back to 0,0
	sys.stdout.write(u"\u001b["+str(N_COL)+"D")
	sys.stdout.write(u"\u001b["+str(N_LIN)+"A")

	# go to line "y"
	if y>0:
		sys.stdout.write(u"\u001b["+str(y)+"B")

	# top border
	if x>0:
		sys.stdout.write(u"\u001b["+str(x)+"C")
	sys.stdout.write(u"\u001b[1D")
	sys.stdout.write(borders[0])
	for i in range(w-2):
		sys.stdout.write(borders[1])
	sys.stdout.write(borders[2])
	sys.stdout.write("\n")

	# side borders
	for i in range(h-2):
		if x>0:
			sys.stdout.write(u"\u001b["+str(x)+"C")
		sys.stdout.write(u"\u001b[1D")
		sys.stdout.write(borders[3])
		if fill_character=="":
			sys.stdout.write(u"\u001b["+str(w-1)+"C")
		else :
			for j in range(w-2):
				sys.stdout.write(fill_character)
		sys.stdout.write(borders[4])
		sys.stdout.write("\n")

	# bottom border
	if x>0:
		sys.stdout.write(u"\u001b["+str(x)+"C")
	sys.stdout.write(u"\u001b[1D")
	sys.stdout.write(borders[5])
	for i in range(w-2):
		sys.stdout.write(borders[6])
	sys.stdout.write(borders[7])
	sys.stdout.write("\n")

	sys.stdout.flush()

# def print_command(command):
# 	#go back to 0,0
# 	sys.stdout.write(u"\u001b["+str(N_COL)+"D")
# 	sys.stdout.write(u"\u001b["+str(N_LIN)+"A")	

# 	sys.stdout.write(u"\u001b["+str(N_LIN-1)+"B")

# 	sys.stdout.flush()

# 	return input(command)


def init_console():
	#resize the console
	os.system('mode con: cols='+str(N_COL)+' lines='+str(N_LIN))
	os.system("color")

	hide_cursor()
	clear()
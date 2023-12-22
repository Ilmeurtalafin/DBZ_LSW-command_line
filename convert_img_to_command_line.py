#! /usr/bin/env python3
# coding=utf-8

import random 
from display import *
from cards import *
from characters import *
import math
import time
import json
import numpy as np
from PIL import Image

tile_size=[8,16]

init_console()

img_colors = Image.open('./data/img_src/palette.png') # Can be many different formats.
# print(img_colors.mode)
palette = img_colors.load()

img_chars = Image.open('./data/img_src/charlist_bw.png') # Can be many different formats.
# print(img_chars.mode)
pix_chars = img_chars.load()



# char_range=range(img_chars.size[0]//tile_size[0])
# char_range=list(range(23,26))+list(range(66,71))#img_chars.size[0]//tile_size[0])
char_range=list(range(66,71))
# char_range=list(range(67,68))
# char_range=list(range(66,67))
# char_range=list(range(23,26))
chars=[img_chars.crop((i*tile_size[0], 0, (i+1)*tile_size[0], tile_size[1])).load() for i in char_range]

char_list_src="!#%&'()*+,-./[_]^_`{|}~░▒▓│┤╡╢╖╕╣║╗╝╜╛┐└┴┬├─┼╞╟╚╔╩╦╠═╬╧╨╤╥╙╘╒╓╫╪┘┌█▄▌▐▀≡⌠⌡≈°■"
char_list=[char_list_src[i] for i in char_range]



def pixelise(img_src):
	pix_src=img_src.load()

	# color_set=set([i for i in range(16)])
	color_set=set()
	image_dic={"tiles":[]}

	# # replace pixel color with closest color in palette
	# for y in range(0,img_src.size[1],1):
	# 	for x in range(0,img_src.size[0],1):
	# 		pix_color=pix_src[x,y]

	# 		best_color=palette[0,0]
	# 		min_diff=257*3
	# 		index_best=0
	# 		for i in range(img_colors.size[0]):
	# 			color=palette[i,0]
	# 			diff=0
	# 			for c in range(3):
	# 				diff+=abs(color[c]-pix_color[c])
	# 			if diff<min_diff:
	# 				min_diff=diff
	# 				best_color=color
	# 				index_best=i
	# 		pix_src[x,y]=best_color
	# # img_src.save('./data/palettized.png')





	for y in range(0,img_src.size[1],4):
		for x in range(0,img_src.size[0],4):
			pix_color=pix_src[x,y]

			best_color=palette[0,0]
			min_diff=257*3
			index_best=0
			for i in range(img_colors.size[0]):
				color=palette[i,0]
				diff=0
				for c in range(3):
					diff+=abs(color[c]-pix_color[c])
				if diff<min_diff:
					min_diff=diff
					best_color=color
					index_best=i
			color_set.add(index_best)

			clear()
			print((x+y*img_src.size[0])/(img_src.size[0]*img_src.size[1]))
			# print(color_set)
			print(len(color_set))

	for v in range(img_src.size[1]//tile_size[1]):
		for u in range(img_src.size[0]//tile_size[0]):
			offset_x=u*tile_size[0]
			offset_y=v*tile_size[1]
			tile_color_acc=[0,0,0]
			for x in range(0,tile_size[0],4):
				for y in range(0,tile_size[1],4):
					for c in range(3):
						tile_color_acc[c]+=pix_src[offset_x+x,offset_y+y][c]
			tile_color=[c//(tile_size[0]*tile_size[1]) for c in tile_color_acc]

			best_color=palette[0,0]
			min_diff=257*3
			index_best=0
			for i in range(img_colors.size[0]):
				color=palette[i,0]
				diff=0
				for c in range(3):
					diff+=abs(color[c]-tile_color[c])
				if diff<min_diff:
					min_diff=diff
					best_color=color
					index_best=i
			color_set.add(index_best)

			clear()
			print((u+v*img_src.size[0]//tile_size[0])/(img_src.size[0]//tile_size[0]*img_src.size[1]//tile_size[1]))
			# print(color_set)
			print(len(color_set))


	print("color set ready")

	for v in range(img_src.size[1]//tile_size[1]):
		for u in range(img_src.size[0]//tile_size[0]):

			offset_x=u*tile_size[0]
			offset_y=v*tile_size[1]

			min_diff=122880
			best_ci=0
			best_c0_index=0
			best_c1_index=0

			for c0 in color_set: #range(img_colors.size[0]): # FG
				color0=palette[c0,0]
				for c1 in color_set: #range(img_colors.size[0]): # BG
					color1=palette[c1,0]

					for ci,char in enumerate(chars):

						diff=0

						for y in range(0,tile_size[1],4):
							for x in range(0,tile_size[0],4):
								char_pix_mask=char[x,y][0]/255.0

								char_pix_colored=[char_pix_mask*color0[c]+(1-char_pix_mask)*color1[c] for c in range(3)]
								for c in range(3):
									diff+=abs(pix_src[offset_x+x,offset_y+y][c]-char_pix_colored[c])

						if diff<min_diff:
							min_diff=diff
							best_ci=ci 
							best_c0_index=c0
							best_c1_index=c1

			image_dic["tiles"]+=[{"x":u,"y":v,"c0_index":best_c0_index,"c1_index":best_c1_index,"char":char_list[best_ci]}]
			sys.stdout.write(u"\u001b[48;5;"+str(best_c1_index)+"m"+u"\u001b[38;5;"+str(best_c0_index)+"m"+char_list[best_ci])
			sys.stdout.flush()
		sys.stdout.write("\n")
	print(ansi_code["Reset"])

	# # old version with solid colors
	# for v in range(img_src.size[1]//tile_size[1]):
	# 	for u in range(img_src.size[0]//tile_size[0]):
	# 		offset_x=u*tile_size[0]
	# 		offset_y=v*tile_size[1]
	# 		tile_color_acc=[0,0,0]
	# 		for x in range(tile_size[0]):
	# 			for y in range(tile_size[1]):
	# 				for c in range(3):
	# 					tile_color_acc[c]+=pix_src[offset_x+x,offset_y+y][c]
	# 		tile_color=[c//(tile_size[0]*tile_size[1]) for c in tile_color_acc]

	# 		best_c0_index=palette[0,0]
	# 		min_diff=257*3
	# 		index_best=0
	# 		for i in range(img_colors.size[0]):
	# 			color=palette[i,0]
	# 			diff=0
	# 			for c in range(3):
	# 				diff+=abs(color[c]-tile_color[c])
	# 			if diff<min_diff:
	# 				min_diff=diff
	# 				best_color=color
	# 				index_best=i


	# 		image_dic["tiles"]+=[{"x":u,"y":v,"c0_index":index_best,"c1_index":index_best,"char":"█"}]
	# 		sys.stdout.write(u"\u001b[48;5;"+str(index_best)+"m ")
	# 	sys.stdout.write("\n")
	# 	sys.stdout.flush()

	return image_dic
	

img_src = Image.open("./data/img_src/VS.png")
pix_src = img_src.load()
image_dic=pixelise(img_src)
with open('./data/output.json', 'w') as fp:
    json.dump(image_dic, fp)

# img_src_array=[Image.open("./data/img_src/bg"+str(i)+".png") for i in range(13)]
# for i,img_src in enumerate(img_src_array):
# 	image_dic=pixelise(img_src)
# 	with open("./data/backgrounds/bg"+str(i)+".json", 'w') as fp:
#    	 json.dump(image_dic, fp)




# sys.stdout.write(ansi_code["Reset"])
# # print(image_dic)

# with open('./data/output.json', 'w') as fp:
#     json.dump(image_dic, fp)

# print(tile_color)
# print(best_color)
# print(index_best)

# # loop waiting for enter key
# while True:
# 	# read one char and get char code
# 	char = ord(msvcrt.getch())

# 	if char in {10, 13}:
# 		break

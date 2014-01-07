#!/usr/bin/python

# on gentoo pillow needs to be installed

import time
import math
import random
from PIL import Image
from mmap import mmap
import struct
import pdb

# see cyclone v device handbook
# Cyclone V Device Handbook
# Volume 3: Hard Processor System Technical Reference Manual

# Address Spaces
FPGASLAVES_OFFSET = 0xC0000000
#FPGASLAVES_SIZE = # 960 MB
LWFPGASLAVES_OFFSET = 0xff200000
#LWFPGASLAVES_SIZE =  #2 MB
PERIPH_OFFSET =  0xFC000000
#PERIPH_SIZE =  #64 MB


def pixel_list(pic):
  # pixelsWide = 32
  # pixelsTall = 16

  im = Image.open(pic)
  # im = im.rotate(180)
  #resize image and rotate
  im = im.rotate(90)
  # im = im.transpose(Image.FLIP_LEFT_RIGHT)
  # half = 0.5
  # im = im.resize( [int(half * s) for s in im.size] )
  #todo: check size. resize if necessary?
  rgb_im = im.convert('RGB')
  # print 'size of picture:', rgb_im.size
  pixels = list(rgb_im.getdata())
  # pixels = list(rgb_im.getdata()) + list(rgb_im.getdata())+list(rgb_im.getdata()) + list(rgb_im.getdata())
  # print len(pixels)
  return pixels


f = open("/dev/mem", "r+b" )
# # mem = mmap(f.fileno(), 0x2000, offset=0xff200000)
mem = mmap(f.fileno(), 0x2000, offset=LWFPGASLAVES_OFFSET+0x2000)
# factor = 0.1
factor = 0.05
# factor = 1.0
shift = 0
# for pixel_nr,position in enumerate(range(0,512*4,4)):
# pdb.set_trace()
# for pixel_nr,position in enumerate(range(0,512*4,4)):
    # mem[position:position+4] = struct.pack("<L", 0x00000000)
    # mem[position:position+4] = struct.pack("<L", 0x000000FF)
    # print pixel_nr, position
for nr, pix in enumerate(mem):
  mem[nr] = struct.pack("<B", 0x00)
# exit(0)

# position = (128+63)*4
# mem[position:position+4] = struct.pack("<L", 0x0000FF00)
# exit(0)
   
# ./text2pixels.py -p --size 18 --bold hello
text =  ['###                      ###   ###             ',
         '###                      ###   ###             ',
        '###                      ###   ###             ',
        '###                      ###   ###             ',
        '###  ###       #####     ###   ###     #####   ',
        '#########    #########   ###   ###   ######### ',
        '####  ####   ###   ###   ###   ###   ###   ### ',
        '###    ###  ###     ###  ###   ###  ###     ###',
        '###    ###  ###########  ###   ###  ###     ###',
        '###    ###  ###########  ###   ###  ###     ###',
        '###    ###  ###          ###   ###  ###     ###',
        '###    ###   ###     ##  ###   ###   ###   ### ',
        '###    ###   ##########  ###   ###   ######### ',
        '###    ###     #######   ###   ###     #####   ']

#/text2pixels.py -p --size 18 --bold H
# text = ['###      ###',
#         '###      ###',
#         '###      ###',
#         '###      ###',
#         '###      ###',
#         '############',
#         '############',
#         '###      ###',
#         '###      ###',
#         '###      ###',
#         '###      ###',
#         '###      ###',
#         '###      ###']

height = 16
width = 32*4

line_offset = 0
# line_offset = width
for line in text:
    
    for nr, pixel in enumerate(line):
        if pixel == '#':
            position = (nr+line_offset)*4
            mem[position:position+4] = struct.pack("<L", 0x0000FF00)
            # print nr, position, line_offset
    line_offset += width
    # print line_offset
exit(0)


while True:    
    for picture in ['SuperMario_step1.png', 'SuperMario_step2.png','SuperMario_step3.png']:
        # pixels = pixel_list('./SuperMarioStanding_02.png')
        pixels = pixel_list(picture)

        for pixel_nr,position in enumerate(range(0,512*4,4)):
          # color = [int(pixel*factor) for pixel in pixels[((pixel_nr+shift*32)%512)]]
          color = [int(pixel*factor) for pixel in pixels[((pixel_nr-shift)%512)]]
          val = int(color[0] + (color[1]<<8) + (color[2]<<16))
          # print val
          # the next line is for the 64x16 fpga image
          position_new = position + ((position>>7) +1)*32*4
          position_new2 = position + ((position>>7))*32*4
          # position_new = position
          mem[position_new:position_new+4] = struct.pack("<L", val)
          mem[position_new2:position_new2+4] = struct.pack("<L", val)
          # mem[position:position+4] = struct.pack("<L", 0x00FFFFFF)

        if shift < 15:
           shift = shift + 1
        else:
           shift = 0
        # shift = shift + 1 if shift < 15 else 0
        time.sleep(0.05)
        # time.sleep(0.01)


#output to file for vhdl initialisation
output = open('output.txt', 'w')
# for item in mem:
#   output.write("%s,\n" % ord(item))

# output.write(",\n".join(mem))
output.write("constant ROM2 : memory := (\n")
output.write(",\n".join(map(lambda x: str(ord(x)), mem)))
output.write("\n);\n")

# position=0
# mem[position:position+4] = struct.pack("<L", 0x000000FF)
# position=128*5*4
# mem[position:position+4] = struct.pack("<L", 0x000000FF)
# position=256*4 
# mem[position:position+4] = struct.pack("<L", 0x0000FF00)

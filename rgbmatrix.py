#!/usr/bin/python

# on gentoo pillow needs to be installed

import time
import math
import random
from PIL import Image
from mmap import mmap
import struct

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
  im = im.rotate(180)
  #todo: check size. resize if necessary?
  rgb_im = im.convert('RGB')
  # print 'size of picture:', rgb_im.size
  pixels = list(rgb_im.getdata())
  return pixels


f = open("/dev/mem", "r+b" )
# # mem = mmap(f.fileno(), 0x2000, offset=0xff200000)
mem = mmap(f.fileno(), 0x2000, offset=LWFPGASLAVES_OFFSET+0x2000)
#mem=[0]*512*4
# factor = 0.0
factor = 0.2
brighter = True
shift = 0
while True:
    # if brighter:
    #     factor += 0.1
    # else:
    #     factor -= 0.1

    # if factor > 1:
    #     brighter = False
    #     factor = 1
    # if factor < 0:
    #     brighter = True
    #     factor = 0
    
    for picture in ['SuperMario_step1.png', 'SuperMario_step2.png','SuperMario_step3.png']:
        # pixels = pixel_list('./SuperMarioStanding_02.png')
        pixels = pixel_list(picture)

        # TODO: there should be a easier way to write the data to the memory
        # check mem.seek(4) 

        for pixel_nr,position in enumerate(range(0,512*4,4)):
          # print pixel_nr, position
          # mem[position:position+4] = struct.pack("<L", 0x00FF00)
          # print pixels[pixel_nr]
          # color = pixels[pixel_nr]
#          color = [int(pixel*factor) for pixel in pixels[pixel_nr]]
#          pixel_anim = ((pixel_nr+shift*32)%512)
#          print pixel_anim
          color = [int(pixel*factor) for pixel in pixels[((pixel_nr+shift*32)%512)]]
          # this looks very ugly
          val = int(color[0] + (color[1]<<8) + (color[2] <<16))
          # print val
          mem[position:position+4] = struct.pack("<L", val)
          # mem[position:position+4] = struct.pack("<L", 0x00FFFFFF)
        if shift < 15:
           shift = shift + 1
        else:
           shift = 0
        time.sleep(0.05)

output = open('output.txt', 'w')
# for item in mem:
#   output.write("%s,\n" % ord(item))

# output.write(",\n".join(mem))
output.write("constant ROM2 : memory := (\n")
output.write(",\n".join(map(lambda x: str(ord(x)), mem)))
output.write("\n);\n")

#!/usr/bin/python

import time
import math
import random
from PIL import Image
from mmap import mmap
import struct

def pixel_list(pic):
  # pixelsWide = 32
  # pixelsTall = 16

  im = Image.open(pic)
  im = im.rotate(180)
  #todo: check size. resize if necessary?
  rgb_im = im.convert('RGB')
  print 'size of picture:', rgb_im.size
  pixels = list(rgb_im.getdata())
  return pixels


f = open("/dev/mem", "r+b" )
mem = mmap(f.fileno(), 0x2000, offset=0xff200000)

# with open("/dev/mem", "r+b" ) as f:
#   # mem = mmap(f.fileno(), 0x04000000, offset=0xfc000000)
#   mem = mmap(f.fileno(), 0x2000, offset=0xff200000)
#   # print hex(len(mem))
#   # mem = mem[0xff200000+0x2000:0xff200000+0x2000+0x2000]
#   # print hex(len(mem))
#   # print mem

# '''print all values'''
# for one in mem:
  # val = struct.unpack("B", one)[0]
  # print val

# mem.seek(0)
# for position in range(0,len(mem),4):
  # print position
  # mem[position:position+4] = struct.pack("<L", 0x00FF00)

# for position, one in enumerate(mem):
#   val = struct.pack("B", 255)
#   # print position
#   # one = val
#   mem[position] = val
#   # mem.write_byte(chr(255))
#   print position, struct.unpack("<B", val)[0], struct.unpack("<B", mem[position])[0]

pixels = pixel_list('./SuperMarioStanding_02.png')
# mem.seek(0)
# data = ''
# for pixel in pixels:
#     # self.i2c.writeList(pixel[0],list(pixel[1:]))
#     # mem.seek(4)
#     data += struct.pack('4B', 0,pixel[2],pixel[1],pixel[0])
# mam = data

# TODO: there should be a easier way to write the data to the memory
# check mem.seek(4) 

for pixel_nr,position in enumerate(range(0,512*4,4)):
  print pixel_nr, position
  # mem[position:position+4] = struct.pack("<L", 0x00FF00)
  print pixels[pixel_nr]
  color = pixels[pixel_nr]
  # this looks very ugly
  val = int(color[0] + (color[1]<<8) + (color[2] <<16))
  print val
  mem[position:position+4] = struct.pack("<L", val)

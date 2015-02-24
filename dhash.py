#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os.path, json
from glob import glob
from PIL import Image

def dhash(image, hash_size=8):
  # Grayscale and shrink the image in one step.
  image = image.convert('L').resize((hash_size + 1, hash_size), Image.ANTIALIAS)

  # pixels = list(image.getdata())

  # Compare adjacent pixels.
  difference = []

  for row in range(hash_size):
    for col in range(hash_size):
      pixel_left = image.getpixel((col, row))
      pixel_right = image.getpixel((col + 1, row))
      difference.append(pixel_left > pixel_right)

  # Convert the binary array to a hexadecimal string.
  decimal_value = 0
  hex_string = []

  for index, value in enumerate(difference):
    if value:
      decimal_value += 2**(index % hash_size)
    if (index % hash_size) == hash_size-1:
      hex_string.append(hex(decimal_value)[2:].rjust(2, '0'))
      decimal_value = 0

  return ''.join(hex_string)

def get_images_from_paths(paths):
  files = []

  for filepath in paths:
    files += glob(filepath)

  return [f for f in files if os.path.isfile(f)]

def data_to_json(data):
  with open('data.json', 'w') as jsonfile:
    json.dump(data, jsonfile)

def calc_dhash_from_files(files):
  result = []

  for image in files:
    img = Image.open(image)
    image_hash = dhash(img)

    result.append({
      "path": image,
      "hash": image_hash
    })

  return result

def main(paths):
  files = get_images_from_paths(paths)
  return calc_dhash_from_files(files)

if __name__ == "__main__":
  if len(sys.argv[1:]) < 1:
    print('Images must be passed as arguments')
    sys.exit()

  print(main(sys.argv[1:]))

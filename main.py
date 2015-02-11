import sys, os.path, json
from PIL import Image

def dhash(image, hash_size = 8):
  # Grayscale and shrink the image in one step.
  image = image.convert('L').resize((hash_size + 1, hash_size), Image.ANTIALIAS)

  pixels = list(image.getdata())

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
      decimal_value += 2**(index % 8)
      if (index % 8) == 7:
        hex_string.append(hex(decimal_value)[2:].rjust(2, '0'))
        decimal_value = 0

  return ''.join(hex_string)

real_images = 0
data = {}

if len(sys.argv[1:]) < 1:
  print('Images must be passed as arguments')
  sys.exit()

for image in sys.argv[1:]:
  print('Checking image: %s' % image)

  print(os.path.isdir(image))


  if not os.path.isfile(image):
    print('Not a image. Proceeding...')
    continue

  real_images += 1
  print('Gererating hash for: %s' % image)
  img = Image.open(image)
  hash = dhash(img)
  data[image] = hash
  print('Hash: %s' % hash)

print('%i images read' % real_images)
print('Writing json')

with open('data.json', 'w') as jsonfile:
  json.dump(data, jsonfile)

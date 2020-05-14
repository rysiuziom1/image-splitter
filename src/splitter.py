import json
import sys
import os
from PIL import Image

image_name = sys.argv[1]
tile_size = sys.argv[2]
resources_path = os.path.join(os.pardir, 'resources')
file = os.path.join(resources_path, image_name)
img = Image.open(file)

img_w, img_h = img.size
tile_w, tile_h = [int(i) for i in tile_size.split('x')]

print('image width:', img_w, 'image height:', img_h)
print('tile width:', tile_w, 'tile height:', tile_h)

if img_w % tile_w != 0 or img_h % tile_h != 0:
    print("Cannot split image using current tile size!")
    sys.exit(1)

h_tiles = int(img_w / tile_w)
v_tiles = int(img_h / tile_h)
file_name, file_extension = os.path.splitext(image_name)
output_directory = os.path.join(resources_path, file_name)
if not os.path.exists(output_directory):
    os.mkdir(output_directory)

with open(os.path.join(resources_path, file_name) + '.json', 'r') as f:
    regions = json.load(f)

for region in regions.items():
    counter = 0
    for i in range(region[1]['start_y'], region[1]['end_y'] + 1):
        for j in range(region[1]['start_x'], region[1]['end_x'] + 1):
            directory = os.path.join(output_directory, str(region[0]))
            if not os.path.exists(directory):
                os.mkdir(directory)
            out_file = os.path.join(directory, str(region[0]) + "_" + str(counter) + file_extension)
            tile = img.crop((j * tile_w, i * tile_h, j * tile_w + tile_w, i * tile_h + tile_h))
            center = tile.size
            center = (center[0] / 2, center[1] / 2)
            center_pixel_alpha = tile.getpixel(center)[3]
            if center_pixel_alpha != 0:
                tile.save(out_file, file_extension.upper()[1:])
                counter += 1

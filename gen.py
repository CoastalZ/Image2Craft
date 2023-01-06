from PIL import Image
from pathlib import Path
from typing import List, Tuple
import math
import os

def classify_rgb_value(rgb: Tuple[int, int, int], defaultRgb: List=[]) -> str:
    closest_distance = float("inf")
    closest_image = None
    if defaultRgb == []:
        average_rgb_values = {'black_concrete.png': (8.40234375, 10.40234375, 15.40234375), 'black_wool.png': (20.6015625, 21.296875, 25.6328125), 'blue_concrete.png': (44.5390625, 46.5390625, 143.421875), 'blue_wool.png': (53.0546875, 57.25390625, 157.4921875), 'brown_concrete.png': (96.44921875, 59.546875, 31.59765625), 'brown_wool.png': (114.234375, 71.609375, 40.5859375), 'cyan_concrete.png': (21.4453125, 119.21875, 136.1875), 'cyan_wool.png': (21.24609375, 137.7265625, 145.3515625), 'gray_concrete.png': (54.6171875, 57.6171875, 61.6171875), 'gray_wool.png': (62.74609375, 68.234375, 71.5546875), 'green_concrete.png': (73.40625, 91.33984375, 36.4921875), 'green_wool.png': (84.83203125, 109.53515625, 27.50390625), 'light_blue_concrete.png': (35.59765625, 137.0390625, 198.9140625), 'light_blue_wool.png': (58.0703125, 175.046875, 217.31640625), 'light_gray_concrete.png': (125.03125, 125.03125, 115.03125), 'light_gray_wool.png': (142.03125, 142.1640625, 134.6015625), 'lime_concrete.png': (94.08984375, 168.8046875, 24.5), 'lime_wool.png': (112.2109375, 185.1953125, 25.796875), 'magenta_concrete.png': (169.20703125, 48.4765625, 159.2109375), 'magenta_wool.png': (189.54296875, 68.765625, 179.91796875), 'orange_concrete.png': (224.34375, 97.13671875, 0.6328125), 'orange_wool.png': (240.65234375, 118.078125, 19.51171875), 'pink_concrete.png': (213.5, 101.01171875, 142.8671875), 'pink_wool.png': (237.9140625, 141.37890625, 172.3515625), 'purple_concrete.png': (100.4140625, 31.62109375, 156.3828125), 'purple_wool.png': (121.875, 42.2109375, 172.5078125), 'red_concrete.png': (142.3828125, 32.8125, 32.8125), 'red_wool.png': (160.96875, 39.3203125, 34.640625), 'white_concrete.png': (207.109375, 213.078125, 214.07421875), 'white_wool.png': (233.58984375, 236.296875, 236.7734375), 'yellow_concrete.png': (240.98828125, 175.41015625, 21.44921875), 'yellow_wool.png': (248.78125, 197.9609375, 39.6328125)}
    elif defaultRgb == ['all']:
        average_rgb_values = {'acacia_planks.png': (168.1328125, 90.37109375, 50.2265625), 'birch_planks.png': (192.46875, 175.29296875, 121.2421875), 'blackstone.png': (42.2109375, 35.5, 40.734375), 'black_concrete.png': (8.40234375, 10.40234375, 15.40234375), 'black_concrete_powder.png': (25.296875, 26.7421875, 31.9765625), 'black_glazed_terracotta.png': (67.734375, 30.03515625, 32.2109375), 'black_terracotta.png': (37.21875, 22.828125, 16.38671875), 'black_wool.png': (20.6015625, 21.296875, 25.6328125), 'blue_concrete.png': (44.5390625, 46.5390625, 143.421875), 'blue_concrete_powder.png': (70.23828125, 73.265625, 166.83203125), 'blue_glazed_terracotta.png': (47.453125, 64.64453125, 139.37109375), 'blue_ice.png': (116.08984375, 167.6484375, 253.015625), 'blue_terracotta.png': (74.29296875, 59.68359375, 91.109375), 'blue_wool.png': (53.0546875, 57.25390625, 157.4921875), 'bricks.png': (150.953125, 97.56640625, 83.0625), 'brown_concrete.png': (96.44921875, 59.546875, 31.59765625), 'brown_concrete_powder.png': (125.53515625, 84.84765625, 53.86328125), 'brown_glazed_terracotta.png': (119.96875, 106.24609375, 85.9453125), 'brown_terracotta.png': (77.234375, 51.1796875, 35.703125), 'brown_wool.png': (114.234375, 71.609375, 40.5859375), 'chiseled_polished_blackstone.png': (53.9765625, 48.6640625, 56.8125), 'coal_block.png': (16.0234375, 15.91796875, 15.91796875), 'copper_block.png': (192.41796875, 107.65625, 79.8203125), 'copper_ore.png': (124.71875, 125.6875, 120.046875), 'crimson_planks.png': (101.03515625, 48.78125, 70.56640625), 'cut_copper.png': (191.171875, 106.8671875, 80.56640625), 'cyan_concrete.png': (21.4453125, 119.21875, 136.1875), 'cyan_concrete_powder.png': (36.6484375, 147.9765625, 157.16015625), 'cyan_glazed_terracotta.png': (52.25, 118.71875, 125.33203125), 'cyan_terracotta.png': (86.71484375, 91.01171875, 91.00390625), 'cyan_wool.png': (21.24609375, 137.7265625, 145.3515625), 'dark_oak_planks.png': (66.66015625, 43.09765625, 20.21875), 'diamond_block.png': (98.1640625, 237.13671875, 228.12109375), 'emerald_block.png': (42.37890625, 203.44921875, 87.80078125), 'exposed_copper.png': (161.078125, 125.703125, 103.93359375), 'exposed_cut_copper.png': (154.66015625, 121.75390625, 101.265625), 'fire_coral_block.png': (163.70703125, 35.1640625, 46.87109375), 'gilded_blackstone.png': (55.60546875, 42.93359375, 38.33203125), 'gold_block.png': (246.41796875, 208.3203125, 61.625), 'gray_concrete.png': (54.6171875, 57.6171875, 61.6171875), 'gray_concrete_powder.png': (76.9453125, 81.10546875, 84.9140625), 'gray_glazed_terracotta.png': (83.09765625, 90.30859375, 93.6484375), 'gray_terracotta.png': (57.78515625, 42.4140625, 35.5625), 'gray_wool.png': (62.74609375, 68.234375, 71.5546875), 'green_concrete.png': (73.40625, 91.33984375, 36.4921875), 'green_concrete_powder.png': (97.1875, 119.12109375, 44.56640625), 'green_glazed_terracotta.png': (117.015625, 142.30859375, 67.421875), 'green_terracotta.png': (76.0078125, 83.2890625, 42.3359375), 'green_wool.png': (84.83203125, 109.53515625, 27.50390625), 'hay_block.png': (165.95703125, 139.12109375, 12.4375), 'honeycomb_block.png': (229.34765625, 148.41015625, 29.5390625), 'ice.png': (145.71875, 183.76171875, 253.97265625), 'iron_block.png': (220.1171875, 220.0078125, 220.0078125), 'jungle_planks.png': (160.44140625, 115.19140625, 80.79296875), 'lapis_block.png': (30.6484375, 67.37109375, 140.109375), 'light_blue_concrete.png': (35.59765625, 137.0390625, 198.9140625), 'light_blue_concrete_powder.png': (74.28125, 180.73046875, 213.36328125), 'light_blue_glazed_terracotta.png': (94.54296875, 164.6171875, 208.921875), 'light_blue_terracotta.png': (113.484375, 108.53125, 137.9921875), 'light_blue_wool.png': (58.0703125, 175.046875, 217.31640625), 'light_gray_concrete.png': (125.03125, 125.03125, 115.03125), 'light_gray_concrete_powder.png': (154.890625, 154.95703125, 148.1875), 'light_gray_glazed_terracotta.png': (144.2578125, 166.0625, 167.953125), 'light_gray_terracotta.png': (135.25390625, 106.8828125, 97.5), 'light_gray_wool.png': (142.03125, 142.1640625, 134.6015625), 'lime_concrete.png': (94.08984375, 168.8046875, 24.5), 'lime_concrete_powder.png': (125.38671875, 189.2734375, 41.90625), 'lime_glazed_terracotta.png': (162.94921875, 197.66796875, 55.2109375), 'lime_terracotta.png': (103.53515625, 117.67578125, 52.796875), 'lime_wool.png': (112.2109375, 185.1953125, 25.796875), 'magenta_concrete.png': (169.20703125, 48.4765625, 159.2109375), 'magenta_concrete_powder.png': (192.7265625, 83.80859375, 184.63671875), 'magenta_glazed_terracotta.png': (208.26953125, 100.41796875, 191.91015625), 'magenta_terracotta.png': (149.66796875, 88.1015625, 108.6796875), 'magenta_wool.png': (189.54296875, 68.765625, 179.91796875), 'mangrove_planks.png': (117.953125, 54.08203125, 48.6640625), 'netherite_block.png': (66.51953125, 61.49609375, 63.87890625), 'oak_planks.png': (162.203125, 130.8203125, 78.62890625), 'orange_concrete.png': (224.34375, 97.13671875, 0.6328125), 'orange_concrete_powder.png': (227.28125, 131.859375, 31.91015625), 'orange_glazed_terracotta.png': (154.77734375, 147.48828125, 91.96484375), 'orange_terracotta.png': (161.59765625, 83.87109375, 37.671875), 'orange_wool.png': (240.65234375, 118.078125, 19.51171875), 'oxidized_copper.png': (82.42578125, 162.66796875, 132.8671875), 'oxidized_cut_copper.png': (79.71875, 153.6171875, 126.4296875), 'packed_ice.png': (141.57421875, 180.01171875, 250.4921875), 'pink_concrete.png': (213.5, 101.01171875, 142.8671875), 'pink_concrete_powder.png': (228.859375, 153.328125, 181.0546875), 'pink_glazed_terracotta.png': (235.15625, 154.984375, 181.5625), 'pink_terracotta.png': (161.92578125, 78.27734375, 78.66796875), 'pink_wool.png': (237.9140625, 141.37890625, 172.3515625), 'polished_blackstone_bricks.png': (48.26953125, 42.52734375, 49.7734375), 'purple_concrete.png': (100.4140625, 31.62109375, 156.3828125), 'purple_concrete_powder.png': (131.921875, 55.67578125, 177.59765625), 'purple_glazed_terracotta.png': (109.87109375, 48.0859375, 152.4921875), 'purple_terracotta.png': (118.4453125, 70.26953125, 86.08984375), 'purple_wool.png': (121.875, 42.2109375, 172.5078125), 'purpur_block.png': (169.91796875, 125.91796875, 169.6796875), 'raw_copper_block.png': (154.35546875, 105.92578125, 79.0859375), 'redstone_block.png': (175.56640625, 24.78125, 5.125), 'red_concrete.png': (142.3828125, 32.8125, 32.8125), 'red_concrete_powder.png': (168.19921875, 54.13671875, 50.625), 'red_glazed_terracotta.png': (181.99609375, 59.58203125, 53.015625), 'red_terracotta.png': (143.109375, 61.01953125, 46.90625), 'red_wool.png': (160.96875, 39.3203125, 34.640625), 'spruce_planks.png': (114.91796875, 84.84375, 48.55859375), 'terracotta.png': (152.1328125, 94.015625, 67.71875), 'warped_planks.png': (43.05078125, 104.87109375, 99.140625), 'weathered_copper.png': (108.296875, 153.00390625, 110.359375), 'weathered_cut_copper.png': (109.37109375, 145.3671875, 107.53125), 'white_concrete.png': (207.109375, 213.078125, 214.07421875), 'white_concrete_powder.png': (225.7265625, 227.4921875, 227.83984375), 'white_glazed_terracotta.png': (188.5, 212.49609375, 202.89453125), 'white_terracotta.png': (209.63671875, 178.03515625, 161.34765625), 'white_wool.png': (233.58984375, 236.296875, 236.7734375), 'yellow_concrete.png': (240.98828125, 175.41015625, 21.44921875), 'yellow_concrete_powder.png': (232.88671875, 199.17578125, 54.76953125), 'yellow_glazed_terracotta.png': (234.34765625, 192.3203125, 88.7109375), 'yellow_terracotta.png': (186.26953125, 133.140625, 35.36328125), 'yellow_wool.png': (248.78125, 197.9609375, 39.6328125)}
    else:
        allrgbvalues = {'acacia_planks.png': (168.1328125, 90.37109375, 50.2265625), 'birch_planks.png': (192.46875, 175.29296875, 121.2421875), 'blackstone.png': (42.2109375, 35.5, 40.734375), 'black_concrete.png': (8.40234375, 10.40234375, 15.40234375), 'black_concrete_powder.png': (25.296875, 26.7421875, 31.9765625), 'black_glazed_terracotta.png': (67.734375, 30.03515625, 32.2109375), 'black_terracotta.png': (37.21875, 22.828125, 16.38671875), 'black_wool.png': (20.6015625, 21.296875, 25.6328125), 'blue_concrete.png': (44.5390625, 46.5390625, 143.421875), 'blue_concrete_powder.png': (70.23828125, 73.265625, 166.83203125), 'blue_glazed_terracotta.png': (47.453125, 64.64453125, 139.37109375), 'blue_ice.png': (116.08984375, 167.6484375, 253.015625), 'blue_terracotta.png': (74.29296875, 59.68359375, 91.109375), 'blue_wool.png': (53.0546875, 57.25390625, 157.4921875), 'bricks.png': (150.953125, 97.56640625, 83.0625), 'brown_concrete.png': (96.44921875, 59.546875, 31.59765625), 'brown_concrete_powder.png': (125.53515625, 84.84765625, 53.86328125), 'brown_glazed_terracotta.png': (119.96875, 106.24609375, 85.9453125), 'brown_terracotta.png': (77.234375, 51.1796875, 35.703125), 'brown_wool.png': (114.234375, 71.609375, 40.5859375), 'chiseled_polished_blackstone.png': (53.9765625, 48.6640625, 56.8125), 'coal_block.png': (16.0234375, 15.91796875, 15.91796875), 'copper_block.png': (192.41796875, 107.65625, 79.8203125), 'copper_ore.png': (124.71875, 125.6875, 120.046875), 'crimson_planks.png': (101.03515625, 48.78125, 70.56640625), 'cut_copper.png': (191.171875, 106.8671875, 80.56640625), 'cyan_concrete.png': (21.4453125, 119.21875, 136.1875), 'cyan_concrete_powder.png': (36.6484375, 147.9765625, 157.16015625), 'cyan_glazed_terracotta.png': (52.25, 118.71875, 125.33203125), 'cyan_terracotta.png': (86.71484375, 91.01171875, 91.00390625), 'cyan_wool.png': (21.24609375, 137.7265625, 145.3515625), 'dark_oak_planks.png': (66.66015625, 43.09765625, 20.21875), 'diamond_block.png': (98.1640625, 237.13671875, 228.12109375), 'emerald_block.png': (42.37890625, 203.44921875, 87.80078125), 'exposed_copper.png': (161.078125, 125.703125, 103.93359375), 'exposed_cut_copper.png': (154.66015625, 121.75390625, 101.265625), 'fire_coral_block.png': (163.70703125, 35.1640625, 46.87109375), 'gilded_blackstone.png': (55.60546875, 42.93359375, 38.33203125), 'gold_block.png': (246.41796875, 208.3203125, 61.625), 'gray_concrete.png': (54.6171875, 57.6171875, 61.6171875), 'gray_concrete_powder.png': (76.9453125, 81.10546875, 84.9140625), 'gray_glazed_terracotta.png': (83.09765625, 90.30859375, 93.6484375), 'gray_terracotta.png': (57.78515625, 42.4140625, 35.5625), 'gray_wool.png': (62.74609375, 68.234375, 71.5546875), 'green_concrete.png': (73.40625, 91.33984375, 36.4921875), 'green_concrete_powder.png': (97.1875, 119.12109375, 44.56640625), 'green_glazed_terracotta.png': (117.015625, 142.30859375, 67.421875), 'green_terracotta.png': (76.0078125, 83.2890625, 42.3359375), 'green_wool.png': (84.83203125, 109.53515625, 27.50390625), 'hay_block.png': (165.95703125, 139.12109375, 12.4375), 'honeycomb_block.png': (229.34765625, 148.41015625, 29.5390625), 'ice.png': (145.71875, 183.76171875, 253.97265625), 'iron_block.png': (220.1171875, 220.0078125, 220.0078125), 'jungle_planks.png': (160.44140625, 115.19140625, 80.79296875), 'lapis_block.png': (30.6484375, 67.37109375, 140.109375), 'light_blue_concrete.png': (35.59765625, 137.0390625, 198.9140625), 'light_blue_concrete_powder.png': (74.28125, 180.73046875, 213.36328125), 'light_blue_glazed_terracotta.png': (94.54296875, 164.6171875, 208.921875), 'light_blue_terracotta.png': (113.484375, 108.53125, 137.9921875), 'light_blue_wool.png': (58.0703125, 175.046875, 217.31640625), 'light_gray_concrete.png': (125.03125, 125.03125, 115.03125), 'light_gray_concrete_powder.png': (154.890625, 154.95703125, 148.1875), 'light_gray_glazed_terracotta.png': (144.2578125, 166.0625, 167.953125), 'light_gray_terracotta.png': (135.25390625, 106.8828125, 97.5), 'light_gray_wool.png': (142.03125, 142.1640625, 134.6015625), 'lime_concrete.png': (94.08984375, 168.8046875, 24.5), 'lime_concrete_powder.png': (125.38671875, 189.2734375, 41.90625), 'lime_glazed_terracotta.png': (162.94921875, 197.66796875, 55.2109375), 'lime_terracotta.png': (103.53515625, 117.67578125, 52.796875), 'lime_wool.png': (112.2109375, 185.1953125, 25.796875), 'magenta_concrete.png': (169.20703125, 48.4765625, 159.2109375), 'magenta_concrete_powder.png': (192.7265625, 83.80859375, 184.63671875), 'magenta_glazed_terracotta.png': (208.26953125, 100.41796875, 191.91015625), 'magenta_terracotta.png': (149.66796875, 88.1015625, 108.6796875), 'magenta_wool.png': (189.54296875, 68.765625, 179.91796875), 'mangrove_planks.png': (117.953125, 54.08203125, 48.6640625), 'netherite_block.png': (66.51953125, 61.49609375, 63.87890625), 'oak_planks.png': (162.203125, 130.8203125, 78.62890625), 'orange_concrete.png': (224.34375, 97.13671875, 0.6328125), 'orange_concrete_powder.png': (227.28125, 131.859375, 31.91015625), 'orange_glazed_terracotta.png': (154.77734375, 147.48828125, 91.96484375), 'orange_terracotta.png': (161.59765625, 83.87109375, 37.671875), 'orange_wool.png': (240.65234375, 118.078125, 19.51171875), 'oxidized_copper.png': (82.42578125, 162.66796875, 132.8671875), 'oxidized_cut_copper.png': (79.71875, 153.6171875, 126.4296875), 'packed_ice.png': (141.57421875, 180.01171875, 250.4921875), 'pink_concrete.png': (213.5, 101.01171875, 142.8671875), 'pink_concrete_powder.png': (228.859375, 153.328125, 181.0546875), 'pink_glazed_terracotta.png': (235.15625, 154.984375, 181.5625), 'pink_terracotta.png': (161.92578125, 78.27734375, 78.66796875), 'pink_wool.png': (237.9140625, 141.37890625, 172.3515625), 'polished_blackstone_bricks.png': (48.26953125, 42.52734375, 49.7734375), 'purple_concrete.png': (100.4140625, 31.62109375, 156.3828125), 'purple_concrete_powder.png': (131.921875, 55.67578125, 177.59765625), 'purple_glazed_terracotta.png': (109.87109375, 48.0859375, 152.4921875), 'purple_terracotta.png': (118.4453125, 70.26953125, 86.08984375), 'purple_wool.png': (121.875, 42.2109375, 172.5078125), 'purpur_block.png': (169.91796875, 125.91796875, 169.6796875), 'raw_copper_block.png': (154.35546875, 105.92578125, 79.0859375), 'redstone_block.png': (175.56640625, 24.78125, 5.125), 'red_concrete.png': (142.3828125, 32.8125, 32.8125), 'red_concrete_powder.png': (168.19921875, 54.13671875, 50.625), 'red_glazed_terracotta.png': (181.99609375, 59.58203125, 53.015625), 'red_terracotta.png': (143.109375, 61.01953125, 46.90625), 'red_wool.png': (160.96875, 39.3203125, 34.640625), 'spruce_planks.png': (114.91796875, 84.84375, 48.55859375), 'terracotta.png': (152.1328125, 94.015625, 67.71875), 'warped_planks.png': (43.05078125, 104.87109375, 99.140625), 'weathered_copper.png': (108.296875, 153.00390625, 110.359375), 'weathered_cut_copper.png': (109.37109375, 145.3671875, 107.53125), 'white_concrete.png': (207.109375, 213.078125, 214.07421875), 'white_concrete_powder.png': (225.7265625, 227.4921875, 227.83984375), 'white_glazed_terracotta.png': (188.5, 212.49609375, 202.89453125), 'white_terracotta.png': (209.63671875, 178.03515625, 161.34765625), 'white_wool.png': (233.58984375, 236.296875, 236.7734375), 'yellow_concrete.png': (240.98828125, 175.41015625, 21.44921875), 'yellow_concrete_powder.png': (232.88671875, 199.17578125, 54.76953125), 'yellow_glazed_terracotta.png': (234.34765625, 192.3203125, 88.7109375), 'yellow_terracotta.png': (186.26953125, 133.140625, 35.36328125), 'yellow_wool.png': (248.78125, 197.9609375, 39.6328125)}
        
        average_rgb_values = {}
        for i in range(len(defaultRgb)):    
            
            file = defaultRgb[i] + '.png'
            
            for key, value in allrgbvalues.items():
                if key == file:
                    average_rgb_values[key] = value
    for file, avg_rgb in average_rgb_values.items():
        
        distance = math.sqrt(sum([(a - b) ** 2 for a, b in zip(rgb, avg_rgb)]))
        
        
        if distance < closest_distance:
            closest_distance = distance
            closest_image = file
    finalname = closest_image.split('.')[0]
    return finalname

def GenerateMcFunction(directory, UseBlocks = []):
    photos = [os.path.join(directory, f) for f in os.listdir(directory)]
    for image in photos:
        image_dir = os.path.dirname(image)
        image_name = os.path.basename(image).lower()
        if UseBlocks == []:
            with open(f"{image_dir}/{image_name.split('.')[0]}.mcfunction", 'w') as f:
                openedim  = Image.open(image)
                image = openedim.convert('RGB')
                for y in range(image.height):
                    for x in range(image.width):

                        colour = classify_rgb_value(image.getpixel((x, y)),)

                        f.write(f'setblock ~-{x} ~ ~-{y} minecraft:{colour}\n')
        

        else:
            with open(f"{image_dir}/{image_name.split('.')[0]}.mcfunction", 'w') as f:
                openedim  = Image.open(image)
                image = openedim.convert('RGB')
                for y in range(image.height):
                    for x in range(image.width):

                        colour = classify_rgb_value(image.getpixel((x, y)), UseBlocks)

                        f.write(f'setblock ~-{x} ~ ~-{y} minecraft:{colour}\n')










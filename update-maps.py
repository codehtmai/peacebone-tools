import csv
from decimal import *
import datetime
import os

today = datetime.datetime.now().strftime("%m-%d-%y")

input_product_filename = 'intermediate2.csv'
initial_maps_filename = 'prices.csv'
renamed_maps_filename = 'prices_{}.csv'.format(today)
output_filename = 'products_final_{}.csv'.format(today)
old_maps_filename = 'prices_06-11-18.csv'

# Rename Prices to today
if os.path.exists(initial_maps_filename):
    os.rename(initial_maps_filename, renamed_maps_filename)

# original tags
product_reader = csv.reader(open(input_product_filename, 'r', encoding='utf-8'))
product_lines = list(product_reader)

assert product_lines[0][13] == 'Variant SKU'  # In case they ever change the CSV format
assert product_lines[0][19] == 'Variant Price'

maps_reader = csv.reader(open(renamed_maps_filename, 'r', encoding='utf-8'))
maps_lines = list(maps_reader)

assert maps_lines[0][0] == 'sku'
assert maps_lines[0][7] == 'retail'
assert maps_lines[0][8] == 'minimum_advertised_price'

maps = dict()
for idx, line in enumerate(maps_lines):
    if idx == 0:
        continue
    sku_val = line[0]
    sku = sku_val[1:]

    retail_val = Decimal(line[7])
    map_val = Decimal(line[8])
    wholesale_val = Decimal(line[9])

    maps[sku] = {"retail": retail_val, "map": map_val, "wholesale": wholesale_val}

# Old MAPs
old_maps_reader = csv.reader(open(old_maps_filename, 'r', encoding='utf-8'))
old_maps_lines = list(old_maps_reader)

old_maps = dict()
for idx, line in enumerate(old_maps_lines):
    if idx == 0:
        continue
    sku_val = line[0]
    sku = sku_val[1:]

    retail_val = Decimal(line[7])
    old_map_val = Decimal(line[8])
    old_wholesale_val = Decimal(line[9])
    old_maps[sku] = {"retail": retail_val, "map": old_map_val, "wholesale": old_wholesale_val}

# End Old Maps

prices_lowered = 0
prices_raised = 0
for idx, line in enumerate(product_lines):
    if idx == 0:
        continue
    sku = line[13]  # SKU Column
    if sku == '':
        continue

    if not sku in maps:
        print("SKU {} not found in EA data".format(sku))
        continue
    price = Decimal(line[19])  # Variant Price column
    retail = maps[sku]['retail']
    map_val = Decimal(maps[sku]['map'])
    wholesale = Decimal(maps[sku]['wholesale'])

    diff = 0
    if sku in old_maps: # No comparison to make if it's a new SKU
        old_wholesale = Decimal(old_maps[sku]['wholesale'])
        diff = wholesale - old_wholesale
        line[19] = price + diff

        if diff > 0:
            prices_raised += 1
        elif diff < 0:
            prices_lowered += 1

    if (price + diff) < map_val:
        print("SKU {} fell below MAP and was corrected".format(sku))
        line[19] = map_val

    # assert not retail < Decimal(maps[sku]['map'])

    # if retail < price:
    #    prices_lowered += 1
    # if retail > price:
    #    prices_raised += 1

    # if retail < map_val:
    #    print("SKU {} has a retail of {}, below MAP of {}".format(sku, retail, map_val))
    #    line[19] = map_val
    # else:
    #    line[19] = retail

print("Prices lowered: {}".format(prices_lowered))
print("Prices raised: {}".format(prices_raised))

writer = csv.writer(open(output_filename, 'w', encoding='utf-8', newline=''))
writer.writerows(product_lines)
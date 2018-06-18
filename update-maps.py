import csv
from decimal import *
import datetime
import os

today = datetime.datetime.now().strftime("%m-%d-%y")

input_product_filename = 'intermediate2.csv'
initial_maps_filename = 'prices.csv'
renamed_maps_filename = 'prices_{}.csv'.format(today)
output_filename = 'products_final_{}.csv'.format(today)

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

    maps[sku] = {"retail": retail_val, "map": map_val}

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

    if price < map_val:
        prices_raised += 1
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

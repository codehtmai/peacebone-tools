import argparse
import csv

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--file", required=True,
                help="Filename to run on")
ap.add_argument("-p", "--published", required=False, action='store_true',
                help="Calculate published stats")
ap.add_argument("-c", "--compare", required=False,
                help="Show new products from -f [file] not in -c [file]")
args = vars(ap.parse_args())

# display a friendly message to the user

published_set = args["published"]

if args["compare"] is not None:
    compare = True
else:
    compare = False

maps_reader = csv.reader(open(args["file"] + ".csv", 'r', encoding='utf-8'))
maps_lines = list(maps_reader)

published_true_count = 0
published_false_count = 0
# total_count = 0
ids = set()
for idx, line in enumerate(maps_lines):
    if idx == 0:
        continue
    ids.add(line[0])
    published = line[6].lower()
    vendor = line[3]

    if published == "true":
        published_true_count += 1
    if published == "false":
        published_false_count += 1
total = idx

if compare:
    compare_reader = csv.reader(open(args["compare"] + ".csv", 'r', encoding='utf-8'))
    compare_lines = list(compare_reader)
    compare_ids = set()
    for idx, line in enumerate(compare_lines):
        if idx == 0:
            continue
        compare_ids.add(line[0])
    new_items = ids - compare_ids
    deleted_items = compare_ids - ids
    print("New items:")
    print("\n".join(list(new_items)))
    print("Deleted items:")
    print("\n".join(list(deleted_items)))
    print("Items in comparison: {}".format(len(compare_ids)))
    print("New IDs in -f: {}".format(len(new_items)))
    print("Deleted Ids: {}".format(len(deleted_items)))

if published_set:
    print("Published = True: {}".format(published_true_count))
    print("Published = False: {}".format(published_false_count))
    print("IDs in primary: {}".format(len(ids)))
    print("Total SKUs: {}".format(total))



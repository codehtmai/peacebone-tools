import pandas as pd
import csv
import os
import datetime

today = datetime.datetime.now().strftime("%m-%d-%y")

basedir = r"C:\Users\codeh\Google Drive\peacebone-tools"
os.chdir(basedir)

tag_maps_filename = 'TagMaps.csv'
initial_export_filename = 'products_export.csv'
product_export_filename = r'Products\products_export_{}.csv'.format(today)
output_filename = 'intermediate1.csv'

if os.path.exists(initial_export_filename):
    os.rename(initial_export_filename, product_export_filename)
    print("Processing {}".format(product_export_filename))

df = pd.read_csv(tag_maps_filename)
map_dict = {}
for index, row in df.iterrows():
    group = row["Group_"]  # The new tag
    delete = row["Delete?"]
    rename = row["Rename"]
    orig_tag = row["Tag"]

    # If it's got Delete, remove it
    if isinstance(delete, str):
        map_dict[orig_tag] = ""

    # If it's got Rename, rename it - supersedes Delete
    if isinstance(rename, str):
        map_dict[orig_tag] = group+rename # "((?!\s?\w\W)|^)("+group + rename + ")(?!\s?\w)"

    # If it was neither, rename normally
    if not isinstance(delete, str) and not isinstance(rename, str):
        assert group is not None
        assert isinstance(group, str)
        map_dict[orig_tag] = group + orig_tag # "((?!\s?\w\W)|^)("+group + orig_tag + ")(?!\s?\w)"

# original tags
r = csv.reader(open(product_export_filename, 'r', encoding='utf-8')) # Here your csv file
lines = list(r)

for idx, line in enumerate(lines):
    if idx == 0:
        continue
    tags = line[5]
    if tags == '': # Skip variants
        continue
    tagslist = tags.split(',')
    tagslist = [x.strip() for x in tagslist]
    replaced_list = []
    for tag in tagslist:
        tag = tag.strip()
        try:
            newtag = map_dict[tag]
        except KeyError:
            print("Missing: " + tag)
            continue
        replaced_list.append(tag)
        replaced_list.append(newtag)

    replaced_list = list(set(replaced_list)) # dedupe
    rejoined = ",".join(replaced_list)
    line[5] = rejoined

    # Change publishing
    published = line[6]
    vendor = line[3]
    if vendor.lower() != 'peacebone':
        line[6] = 'TRUE'


writer = csv.writer(open(output_filename, 'w', encoding='utf-8', newline=''))
writer.writerows(lines)


#df.loc[df['Tag'] == 'Zukes']

#export_df = pd.read_csv(product_export_filename)

#export_df.Tags.replace(value=map_dict, inplace=True, regex=True)

#export_df.to_csv(output_filename)


# # Filter out missing titles
# export_df2 = (export_df.loc[export_df['Title'].notna()])
# export_df3 = (export_df2.loc[export_df2['Tags'].notna()])
#
# export_tags = []
# errors = []
# for index, row in export_df3.iterrows():
#     title = row['Title']
#     row_tags = row['Tags']
#
#     export_tag_vals = row_tags.split(',')
#     export_tags = export_tags + export_tag_vals
#
#     for tag in export_tag_vals:
#         tag = tag.strip()
#         try:
#             new_tag = dict[tag]
#         except KeyError:
#             #print(tag)
#             errors.append(tag)
#
# errors = list(set(errors))
# errors.sort()
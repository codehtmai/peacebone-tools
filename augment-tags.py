import pandas as pd
import csv
import math

input_filename = 'intermediate1.csv'
output_filename = 'intermediate2.csv'

# original tags
r = csv.reader(open(input_filename, 'r', encoding='utf-8')) # Here your csv file
lines = list(r)

idx = 0
for line in lines:
    if idx == 0:
        idx = 1
        continue
    tags = line[5]
    if tags == '':
        continue
    tagslist = tags.split(',')

    compare_list = [x.lower() for x in tagslist]
    if 'foods_dry food' in compare_list and not "foods_freeze-dried" in compare_list:
        new_tag = "Foods_Kibble"
        tags += ',' + new_tag
        print("Found Kibble on line " + str(idx))
    if 'wet foods_wet food' in compare_list:
        new_tag = "Foods_Wet Food"
        tags += ',' + new_tag
        print("Found wet food on line " + str(idx))
    line[5] = tags
    idx += 1

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
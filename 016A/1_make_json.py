import os
path = "/Volumes/RESEARCH_HD/016/raw_data"
os.chdir(path)
os.listdir() #!ls

# 1 read in original MnA file #
import pandas as pd
event_file = pd.ExcelFile('016MnA_11022018.xls') # manually set the date cells to DATE format
print(event_file.sheet_names)

event_file_1 = pd.read_excel('016MnA_11022018.xls', sheet_name='Request 2', header=1)
event_file_1.columns = event_file_1.columns.str.replace('\n', ' ')
event_file_1[['Acquiror 6-digit CUSIP', 'Date Announced']].head()

# 2 output and cucips to permno #
event_file_1[['Acquiror 6-digit CUSIP']].to_csv('cusips.txt', header=True, index=False, sep='\t', mode='a')
# then go wrds to convert to permno: https://wrds-web.wharton.upenn.edu/wrds/ds/crsp/tools_a/dse/translate/index.cfm?navId=131
convert_table = pd.read_csv('8836874c2a2bcb0d.csv')

# 3 merge permno with MnA file and output json
convert_table['Acquiror 6-digit CUSIP'] = convert_table['NCUSIP'].str.slice(0, 6)
merged = pd.merge(event_file_1[['Acquiror 6-digit CUSIP', 'Date Announced']], convert_table, on=['Acquiror 6-digit CUSIP'], how='inner')
output = merged[['PERMNO', 'Date Announced']]
output.drop_duplicates(keep='first', inplace=True)
output = output.dropna()

output = output.rename(index=str, columns={'Date Announced': 'edate', 'PERMNO': 'permno'})
output['edate'] = output['edate'].dt.strftime('%m/%d/%Y')

import json # https://stackoverflow.com/questions/26745519/converting-dictionary-to-json-in-python
loaded_r = json.loads(json.dumps(output.to_dict('records')))
with open('data.json', 'w') as outfile:
    json.dump(loaded_r, outfile)



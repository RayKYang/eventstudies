# after getting the .xls file from wrds cloud

import os
os.chdir('/Users/Ray_Mac/Documents/R Yang/Py_Projects/Research_Eventstudies/016A')

# 1 get abnormal return by day from the resulting xls
import pandas as pd
# pd.set_option('display.width', 320)
pd.set_option("display.max_columns", 10)

# df_1 = pd.read_excel('EventStudy.xls', sheet_name='Stats')
df_2 = pd.read_excel('EventStudy.xls', sheet_name='Event Window')
# df_3 = pd.read_excel('EventStudy.xls', sheet_name='Event Date')

result = df_2.drop(['rdate', 'ret'], axis=1) # print(result.head())

# 2 get cummulative abnormal return with specified window
def get_car(window):
    # test #
    # window_21 = list(range(-10, 11, 1))
    # window = window_21
    c_abret = result.loc[result['evttime'].isin(window)].groupby(['permno']).sum().drop('evttime', axis=1)
    c_abret['Date Announced'] = result.loc[result['evttime'].isin(window)].groupby(['permno']).last().edate
    c_abret['PERMNO'] = c_abret.index
    c_abret = c_abret.iloc[:, [2,1, 0]]
    return c_abret
    # get_car(window_21) # for test

# windows 0 ~ 11
car_result = get_car([0])
n_windows = 11 # how many window cols do you want?
for w in range(1, n_windows):
    window = list(range(-w, w+1, 1))
    car_result = pd.merge(car_result, get_car(window), on=['PERMNO', 'Date Announced'], how='inner')

car_result.columns = list(car_result.columns[:2]) + list(map('CAR_win_{}'.format, range(1, n_windows*2, 2)))

# 3 merge with cusip and export file
os.chdir("/Volumes/RESEARCH_HD/016/raw_data")
merged = pd.read_csv("cusip_permno_match.csv", parse_dates=['Date Announced'])

merged_ = pd.merge(merged[['Acquiror 6-digit CUSIP', 'Date Announced', 'PERMNO']], car_result,
                  on=['PERMNO', 'Date Announced'], how='right')
merged_.drop_duplicates(keep='first', inplace=True)
merged_.to_csv("carfile_Py.csv", index=False)

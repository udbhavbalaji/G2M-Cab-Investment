#%%
# Importing required libraries
from typing import ValuesView
import pandas as pd
import numpy as np
from pandas.core.accessor import register_index_accessor
from pandas.core.base import DataError
pd.set_option("display.max_columns", None)
# %%
# Loading in all the datasets
cab_data = pd.read_csv('Datasets/Cab_Data.csv')
city = pd.read_csv('Datasets/City.csv')
customer = pd.read_csv('Datasets/Customer_ID.csv')
transaction = pd.read_csv('Datasets/Transaction_ID.csv')
# %%
# Renaming columns
cab_data.columns = ['txnID', 'travel_date', 'company', 'city', 'distance',
       'price', 'cost']
# %%
# Calculating profits from price and cost
cab_data['profit'] = cab_data.price - cab_data.cost
# %%
# Updating date to new format so we know the actual date of each ride
date_list = list(cab_data.travel_date.unique())
date_list.sort()
updated_date = []
i = 0
for date in date_list:
    updated_date.append(i)
    i += 1
list_date = []
j = 0
# for i in range(len(updated_date)):
#     cab_data['travel_date'] = cab_data.travel_date.apply(lambda x: updated_date[i] if x == date_list[i] else x)
for index, row in cab_data.iterrows():
    idx = date_list.index(row['travel_date'])
    list_date.append(updated_date[idx])

cab_data['travel_date'] = list_date
# %%
# Calculating year for each ride
cab_data['year'] = cab_data.travel_date
cab_data['year'] = cab_data.year.apply(lambda x: 2016 if x//365 == 0 else x)
cab_data['year'] = cab_data.year.apply(lambda x: 2017 if x//365 == 1 else x)
cab_data['year'] = cab_data.year.apply(lambda x: 2018 if x//365 == 2 else x)
months = ['January','February','March','April','May','June','July','August','September','October','November','December']
cab_data['date_of_year'] = cab_data.travel_date.apply(lambda x: (x%365)+1)
# %%
# Calculating month and date for each ride
cab_data['month'] = ''
cab_data['date_of_month'] = 0
cab_data['month'] = cab_data.apply(lambda x: 'January' if 1 <= x['date_of_year'] <= 31 else x['month'], axis=1)
cab_data['date_of_month'] = cab_data.apply(lambda x: x['date_of_year']%32 if x['month'] == 'January' else x['date_of_month'], axis = 1)

cab_data['month'] = cab_data.apply(lambda x: 'February' if 32 <= x['date_of_year'] <= 59 else x['month'], axis=1)
cab_data['date_of_month'] = cab_data.apply(lambda x: (x['date_of_year']-31)%29 if x['month'] == 'February' else x['date_of_month'], axis = 1)

cab_data['month'] = cab_data.apply(lambda x: 'March' if 60 <= x['date_of_year'] <= 90 else x['month'], axis=1)
cab_data['date_of_month'] = cab_data.apply(lambda x: (x['date_of_year']-59)%32 if x['month'] == 'March' else x['date_of_month'], axis = 1)

cab_data['month'] = cab_data.apply(lambda x: 'April' if 91 <= x['date_of_year'] <= 120 else x['month'], axis=1)
cab_data['date_of_month'] = cab_data.apply(lambda x: (x['date_of_year']-90)%31 if x['month'] == 'April' else x['date_of_month'], axis = 1)

cab_data['month'] = cab_data.apply(lambda x: 'May' if 121 <= x['date_of_year'] <= 151 else x['month'], axis=1)
cab_data['date_of_month'] = cab_data.apply(lambda x: (x['date_of_year']-120)%32 if x['month'] == 'May' else x['date_of_month'], axis = 1)

cab_data['month'] = cab_data.apply(lambda x: 'June' if 152 <= x['date_of_year'] <= 181 else x['month'], axis=1)
cab_data['date_of_month'] = cab_data.apply(lambda x: (x['date_of_year']-151)%31 if x['month'] == 'June' else x['date_of_month'], axis = 1)

cab_data['month'] = cab_data.apply(lambda x: 'July' if 182 <= x['date_of_year'] <= 212 else x['month'], axis=1)
cab_data['date_of_month'] = cab_data.apply(lambda x: (x['date_of_year']-181)%32 if x['month'] == 'July' else x['date_of_month'], axis = 1)

cab_data['month'] = cab_data.apply(lambda x: 'August' if 213 <= x['date_of_year'] <= 243 else x['month'], axis=1)
cab_data['date_of_month'] = cab_data.apply(lambda x: (x['date_of_year']-212)%32 if x['month'] == 'August' else x['date_of_month'], axis = 1)

cab_data['month'] = cab_data.apply(lambda x: 'September' if 244 <= x['date_of_year'] <= 273 else x['month'], axis=1)
cab_data['date_of_month'] = cab_data.apply(lambda x: (x['date_of_year']-243)%31 if x['month'] == 'September' else x['date_of_month'], axis = 1)

cab_data['month'] = cab_data.apply(lambda x: 'October' if 274 <= x['date_of_year'] <= 304 else x['month'], axis=1)
cab_data['date_of_month'] = cab_data.apply(lambda x: (x['date_of_year']-273)%32 if x['month'] == 'October' else x['date_of_month'], axis = 1)

cab_data['month'] = cab_data.apply(lambda x: 'November' if 305 <= x['date_of_year'] <= 334 else x['month'], axis=1)
cab_data['date_of_month'] = cab_data.apply(lambda x: (x['date_of_year']-304)%31 if x['month'] == 'November' else x['date_of_month'], axis = 1)

cab_data['month'] = cab_data.apply(lambda x: 'December' if 335 <= x['date_of_year'] <= 365 else x['month'], axis=1)
cab_data['date_of_month'] = cab_data.apply(lambda x: (x['date_of_year']-334)%32 if x['month'] == 'December' else x['date_of_month'], axis = 1)

# %%
# Calculating day for each ride
cab_data['day'] = ''
list_days = ['Friday','Saturday','Sunday','Monday','Tuesday','Wednesday','Thursday']
day_list = []
for index, row in cab_data.iterrows():
    idx = row['travel_date']%7
    day_list.append(list_days[idx])
cab_data['day'] = day_list
# %%
# Separating city and state where each ride took place
cab_data['state'] = cab_data.city.apply(lambda x: x[-2:].strip() if x[-3] == ' ' else x.strip())
cab_data['city'] = cab_data.city.apply(lambda x: x[:-2].strip() if x[-3] == ' ' else x.strip())
cab_data.head()
# %%
# Copying the required columns from cab_data into a master data frame
# The required columns are ['txnID','date','day','month','year','city','state','distance','cost','price','profit','company']
master = cab_data[['txnID','date_of_month','day','month','year','city','state','distance','cost','price','profit','company']]
# master = master.set_index('txnID')
master.columns = ['txnID','date','day_name','month','year','city','state','distance','cost','price','profit','company']
master.head()
# %%
# Removing the commas from the population and users and converting to int
city.columns = ['city','population','users']
city['population'] = city.population.apply(lambda x: int(x.replace(',','').strip()))
city['users'] = city.users.apply(lambda x: int(x.replace(',','').strip()))
city.head()
# %%
# Adding the population and num of users of each city to their respective rows
city_list = list(city.city.unique())
pop_dict = {}
user_dict = {}
for region in city_list:
    pop_dict[region] = city[city.city == region]['population'].values[0]
    user_dict[region] = city[city.city == region]['users'].values[0]
pop_dict
pop_list = []
user_list = []
for index, row in master.iterrows():
    user_list.append(user_dict[row['city']])
    pop_list.append(pop_dict[row['city']])
master['population'] = pop_list
master['user'] = user_list
master.head()
# %%

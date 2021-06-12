#%%
# Importing required libraries
from typing import ValuesView
import pandas as pd
import numpy as np
from pandas.core.accessor import register_index_accessor
pd.set_option("display.max_columns", None)
# %%
# Loading in all the datasets
cab_data = pd.read_csv('Datasets/Cab_Data.csv')
city = pd.read_csv('Datasets/City.csv')
customer = pd.read_csv('Datasets/Customer_ID.csv')
transaction = pd.read_csv('Datasets/Transaction_ID.csv')
# %%
cab_data.columns
# %%
# Renaming columns
cab_data.columns = ['txnID', 'travel_date', 'company', 'city', 'distance',
       'price', 'cost']
cab_data.head()
# %%
# Calculating profits from price and cost
cab_data['profit'] = cab_data.price - cab_data.cost
cab_data.head(8)
# %%
# Updating date to new format so we know the actual date of each ride
date_list = list(cab_data.travel_date.unique())
date_list.sort()
updated_date = []
i = 0
for date in date_list:
    updated_date.append(i)
    i += 1
for i in range(len(updated_date)):
    cab_data['travel_date'] = cab_data.travel_date.apply(lambda x: updated_date[i] if x == date_list[i] else x)
cab_data.head()
# %%
# Calculating year for each ride
cab_data['year'] = cab_data.travel_date
cab_data['year'] = cab_data.year.apply(lambda x: 2016 if x//365 == 0 else x)
cab_data['year'] = cab_data.year.apply(lambda x: 2017 if x//365 == 1 else x)
cab_data['year'] = cab_data.year.apply(lambda x: 2018 if x//365 == 2 else x)
months = ['January','February','March','April','May','June','July','August','September','October','November','December']
cab_data['date_of_year'] = cab_data.travel_date.apply(lambda x: x%365)
# %%
# Calculating month for each ride
cab_data['month'] = ''
cab_data['month'] = cab_data.apply(lambda x: 'January' if 0 <= x['date_of_year'] <= 30 else x['month'], axis=1)
cab_data['month'] = cab_data.apply(lambda x: 'February' if 31 <= x['date_of_year'] <= 58 else x['month'], axis=1)
cab_data['month'] = cab_data.apply(lambda x: 'March' if 59 <= x['date_of_year'] <= 89 else x['month'], axis=1)
cab_data['month'] = cab_data.apply(lambda x: 'April' if 90 <= x['date_of_year'] <= 119 else x['month'], axis=1)
cab_data['month'] = cab_data.apply(lambda x: 'May' if 120 <= x['date_of_year'] <= 150 else x['month'], axis=1)
cab_data['month'] = cab_data.apply(lambda x: 'June' if 151 <= x['date_of_year'] <= 180 else x['month'], axis=1)
cab_data['month'] = cab_data.apply(lambda x: 'July' if 181 <= x['date_of_year'] <= 211 else x['month'], axis=1)
cab_data['month'] = cab_data.apply(lambda x: 'August' if 212 <= x['date_of_year'] <= 242 else x['month'], axis=1)
cab_data['month'] = cab_data.apply(lambda x: 'September' if 243 <= x['date_of_year'] <= 272 else x['month'], axis=1)
cab_data['month'] = cab_data.apply(lambda x: 'October' if 273 <= x['date_of_year'] <= 303 else x['month'], axis=1)
cab_data['month'] = cab_data.apply(lambda x: 'November' if 304 <= x['date_of_year'] <= 333 else x['month'], axis=1)
cab_data['month'] = cab_data.apply(lambda x: 'December' if 334 <= x['date_of_year'] <= 364 else x['month'], axis=1)
cab_data.head()
# %%
# Calculating day for each ride

# %%
# Copying cab_data into a master data frame
master = cab_data.copy()
master = master.set_index('txnID')
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

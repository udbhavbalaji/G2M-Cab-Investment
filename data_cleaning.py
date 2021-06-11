#%%
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
cab_data.head()
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

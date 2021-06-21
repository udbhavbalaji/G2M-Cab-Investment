#%%
import pandas as pd
import numpy as np
import datetime
import xlrd
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
# Updating the date from excel serial date fomrat into a common format
cab_data['travel_date'] = cab_data.travel_date.apply(lambda x: xlrd.xldate_as_datetime(x, 0).date())
cab_data.head()
# %%
# Obtaining date, month and year from the travel_date
cab_data['year'] = cab_data.travel_date.apply(lambda x: x.year)
cab_data['month'] = cab_data.travel_date.apply(lambda x: x.month)
cab_data['date'] = cab_data.travel_date.apply(lambda x: x.day)
cab_data.head()
# %%
# Renaming the month in words as it is easier to understand
months = ['January','February','March','April','May','June','July','August','September','October','November','December']
cab_data['month'] = cab_data.month.apply(lambda x: months[x-1])
cab_data.head()
# %%
# Getting the day name of each day
cab_data['day_name'] = cab_data.travel_date.apply(lambda x: x.strftime('%A'))
cab_data.head()
# %%
# Separating city and state where each ride took place
cab_data['city_state'] = cab_data.city
cab_data['state'] = cab_data.city.apply(lambda x: x[-2:].strip() if x[-3] == ' ' else 'CA')
cab_data['city'] = cab_data.city.apply(lambda x: x[:-2].strip() if x[-3] == ' ' else x.strip())
cab_data.head()
# %%
# Copying the required columns from cab_data into a master data frame
# The required columns are ['txnID','date','day','month','year','city','state','distance','cost','price','profit','company']
master = cab_data[['txnID','date','day_name','month','year','city','state','distance','cost','price','profit','company','city_state']]
master.columns = ['txnID','date','day_name','month','year','city','state','distance','cost','price','profit','company','city_state']
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
    user_list.append(user_dict[row['city_state']])
    pop_list.append(pop_dict[row['city_state']])
master['population'] = pop_list
master['user'] = user_list
master.drop('city_state', axis=1, inplace=True)
master.head()
# %%
# Using the transactions data to add relevant columns to master
transaction.columns = ['txnID','custID','pay_mode']
# %%
# Now, we need to map this data to the master data as there are more rows in 
# transactions than in master so we need to map the correct transactions only
master = pd.merge(master, transaction[['custID','pay_mode']], how='left', left_index=True, right_index=True)
# %%
# Adding the customer details to the master set
customer.columns = ['custID','gender','age','monthly_income']
cust_dict = {}
customer = customer.set_index('custID')
for index, row in customer.iterrows():
    cust_dict[index] = [row['gender'], row['age'], row['monthly_income']]
gender_list = []
age_list = []
income_list = []
for index, row in master.iterrows():
    gender_list.append(cust_dict[row['custID']][0])
    age_list.append(cust_dict[row['custID']][1])
    income_list.append(cust_dict[row['custID']][2])
master['gender'] = gender_list
master['age'] = age_list
master['monthly_income'] = income_list
master.head()
# %%
# Re-ordering the columns to make the information more intuitive
master = master[['txnID', 'custID', 'date', 'month', 'year', 'day_name', 'distance', 'city', 'state',
        'cost', 'price', 'profit', 'population', 'user',
        'pay_mode', 'gender', 'age', 'monthly_income', 'company']]
# %%
# We now use the holiday list to add it to the master data
holiday = pd.read_csv('Datasets/USHolidays.csv')
hol2016 = pd.DataFrame(holiday[['Holiday','2016']])
hol2017 = pd.DataFrame(holiday[['Holiday','2017']])
hol2018 = pd.DataFrame(holiday[['Holiday','2018']])
# %%
# 2016
hol2016['date'] = hol2016['2016'].apply(lambda x: int(str(x).split('/')[0]))
hol2016['month'] = hol2016['2016'].apply(lambda x: int(str(x).split('/')[1]))
hol2016['year'] = hol2016['2016'].apply(lambda x: int(str(x).split('/')[2]))
hol2016['month'] = hol2016['month'].apply(lambda x: months[x-1])
# %%
# 2017
hol2017['date'] = hol2017['2017'].apply(lambda x: int(str(x).split('/')[0]))
hol2017['month'] = hol2017['2017'].apply(lambda x: int(str(x).split('/')[1]))
hol2017['year'] = hol2017['2017'].apply(lambda x: int(str(x).split('/')[2]))
hol2017['month'] = hol2017['month'].apply(lambda x: months[x-1])
# %%
# 2018
hol2018['date'] = hol2018['2018'].apply(lambda x: int(str(x).split('/')[0]))
hol2018['month'] = hol2018['2018'].apply(lambda x: int(str(x).split('/')[1]))
hol2018['year'] = hol2018['2018'].apply(lambda x: int(str(x).split('/')[2]))
hol2018['month'] = hol2018['month'].apply(lambda x: months[x-1])
# %%
# Dropping the columns that we no longer need
hol2016.drop('2016', axis=1, inplace=True)
hol2017.drop('2017', axis=1, inplace=True)
hol2018.drop('2018', axis=1, inplace=True)
# %%
# Adding the holiday data into a single dataframe
holidays = hol2016.append(hol2017, ignore_index=True)
holidays = holidays.append(hol2018, ignore_index=True)
# %%
# Adding the holidays to the master dataset
holiday_list = []
for index, row in master.iterrows():
    date = row['date']
    month = row['month']
    year = row['year']
    req_hols = holidays[(holidays.date == date) & (holidays.month == month) & (holidays.year == year)]
    if req_hols.shape[0] == 1:
        holiday_list.append(req_hols.Holiday.values[0])
    else:
        holiday_list.append(np.nan)

master['Holiday'] = holiday_list
# %%
# Final review of the data before exporting into csv file
master.head()
# %%
# Exporting the master data into a csv file to proceed to the EDA
master.to_csv('Datasets/Master_Data.csv', index=False)
# %%
# # # END OF FILE
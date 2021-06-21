#%%
# Importing the required modules
from os import replace
import pandas as pd
import numpy as np
import scipy.stats as stats
# %%
# # Hypotheses:
# 1. Average profit has increased in 2017 compared to 2016
# 2. Average profit is higher on holidays than on regular holidays
# 3. People with a higher income (>= $10000) travel a smaller distance on average
# 4. The average age of card payers is lower than the average age of cash payers
# 5. The average price of rides on week-days is lower than on weekends
# %%
# Reading in the master data
master = pd.read_csv('Datasets/Master_Data.csv')
# %%
# Creating a function for doing the hypothesis testing
def test_hypo(sample1, sample2, alpha=0.05, null='', alternate='', alternative='two-sided'):
    if len(sample1) != len(sample2):
        return
    df = len(sample1)-1
    t_stat, pval = stats.ttest_ind(sample1, sample2, equal_var=False, alternative=alternative)
    if pval < alpha:
        print('There is significant statistical evidence to reject the Null Hypothesis (H0: {})'.format(null))
    else:
        print('There isn\'t significant statistical evidence to reject the Null Hypothesis (H0: {})'.format(null))
        print('Therefore, the Alternate Hypothesis cannot be accepted (Ha: {})'.format(alternate))
    print('t-Statistic Value = {}\nP-Value = {}'.format(t_stat, pval))
#%%
# Average Profit has increased in 2017 compared to 2016
# H0: Avg. profit of 2017 = Avg. profit of 2016
# Ha: Avg. profit of 2017 > Avg. profit of 2016
df_2016 = master[master.year == 2016]
df_2017 = master[master.year == 2017]
random_2016 = df_2016.profit.sample(n=1000)
random_2017 = df_2017.profit.sample(n=1000)
list_2016 = list(random_2016.values)
list_2017 = list(random_2017.values)
# %%
# Running the hypothesis test for test 1
null = 'Avg. profit of 2017 = Avg. profit of 2016'
alternate = 'Avg. profit of 2017 > Avg. profit of 2016'
test_hypo(list_2016, list_2017, alpha=0.05, null=null, alternate=alternate, alternative='greater')
# %%
# Average profit is higher on regular days than on holidays
# H0: Avg. profit on regular days = Avg. profit on Holidays
# Ha: Avg. profit on regular days > Avg. profit on Holidays
reg_df = master[master.Holiday.isnull()]
hol_df = master[~master.Holiday.isnull()]
random_reg = reg_df.profit.sample(n=1000)
random_hol = hol_df.profit.sample(n=1000)
list_reg = list(random_reg.values)
list_hol = list(random_hol)
#%%
# Running the hypothesis test for test 2
null = 'Avg. profit on regular days = Avg. profit on Holidays'
alternate = 'Avg. profit on regular days > Avg. profit on Holidays'
test_hypo(list_reg, list_hol, alpha=0.05, null=null, alternate=alternate, alternative='greater')
# %%
# People with a higher income (>= $10000) travel a smaller distance on average
# H0: Avg. distance travelled by people with (income >= 10000) = Avg. distance travelled by people with (income < 10000)
# Ha: Avg. distance travelled by people with (income >= 10000) < Avg. distance travelled by people with (income < 10000)
high_df = master[master.monthly_income >= 10000]
low_df = master[master.monthly_income < 10000]
random_high = high_df.distance.sample(n=1000)
random_low = low_df.distance.sample(n=1000)
list_high = list(random_high.values)
list_low = list(random_low.values)
# %%
# Running the hypothesis test for test 3
null = 'Avg. distance travelled by people with (income >= 10000) = Avg. distance travelled by people with (income < 10000)'
alternate = 'Avg. distance travelled by people with (income >= 10000) < Avg. distance travelled by people with (income < 10000)'
test_hypo(list_high, list_low, alpha=0.05, null=null, alternate=alternate, alternative='less')
# %%
# # # WILL CONTINUE FOR REST TOMORROW
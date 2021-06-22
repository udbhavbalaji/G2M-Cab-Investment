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
# 4. The average age of card payers is higher than the average age of cash payers
# 5. The average price of rides on week-days is lower than on weekends
# 6. The average distance travelled by the Yellow cabs is greater than the the average distance travelled by the Pink cabs
# %%
# Reading in the master data
master = pd.read_csv('Datasets/Master_Data.csv')
alphas = [0.01,0.05,0.1]
# %%
# Creating a display function to properly output the required results
def disp(null, alternate, hypothesis):
    print('Hypothesis: {}'.format(hypothesis))
    print()
    print('H0: {}'.format(null))
    print('Ha: {}'.format(alternate))
    print()

#%%
# Creating a function for doing the hypothesis testing
def test_hypo(sample1, sample2, alpha=0.05, alternative='two-sided'):
    if len(sample1) != len(sample2):
        return
    print('Alpha: {}'.format(alpha))
    df = len(sample1)-1
    t_stat, pval = stats.ttest_ind(sample1, sample2, equal_var=False, alternative=alternative)
    if pval < alpha:
        print('There is significant statistical evidence to reject the Null Hypothesis')
    else:
        print('There isn\'t significant statistical evidence to reject the Null Hypothesis')
        print('Therefore, the Alternate Hypothesis cannot be accepted.')
    print()
    return t_stat, pval
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
hypothesis = 'Average Profit has increased in 2017 compared to 2016'
null = 'Avg. profit of 2017 = Avg. profit of 2016'
alternate = 'Avg. profit of 2017 > Avg. profit of 2016'
disp(null, alternate, hypothesis)
for alpha in alphas:    
    t_stat, pval = test_hypo(list_2016, list_2017, alpha=alpha, alternative='greater')
print()
print('t-Statistic Value: {}\nP-Value: {}'.format(t_stat, pval))
print()
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
hypothesis = 'Average profit is higher on regular days than on holidays'
null = 'Avg. profit on regular days = Avg. profit on Holidays'
alternate = 'Avg. profit on regular days > Avg. profit on Holidays'
disp(null, alternate, hypothesis)
for alpha in alphas:    
    t_stat, pval = test_hypo(list_reg, list_hol, alpha=alpha, alternative='greater')
print()
print('t-Statistic Value: {}\nP-Value: {}'.format(t_stat, pval))
print()
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
hypothesis = 'People with a higher income (>= $10000) travel a smaller distance on average'
null = 'Avg. distance travelled by people with (income >= 10000) = Avg. distance travelled by people with (income < 10000)'
alternate = 'Avg. distance travelled by people with (income >= 10000) < Avg. distance travelled by people with (income < 10000)'
disp(null, alternate, hypothesis)
for alpha in alphas:    
    t_stat, pval = test_hypo(list_high, list_low, alpha=alpha, alternative='less')
print()
print('t-Statistic Value: {}\nP-Value: {}'.format(t_stat, pval))
print()
# %%
# The average age of card payers is higher than the average age of cash payers
# H0: Avg. age of card payers = Avg. age of cash payers
# Ha: Avg. age of card payers > Avg. age of cash payers
card_df = master[master.pay_mode == 'Card']
cash_df = master[master.pay_mode == 'Cash']
random_card = card_df.age.sample(n=1000)
random_cash = cash_df.age.sample(n=1000)
list_card = list(random_card.values)
list_cash = list(random_cash.values)
# %%
# Running the hypothesis test for test 4
hypothesis = 'The average age of card payers is higher than the average age of cash payers'
null = 'Avg. age of card payers = Avg. age of cash payers)'
alternate = 'Avg. age of card payers > Avg. age of cash payers'
disp(null, alternate, hypothesis)
for alpha in alphas:    
    t_stat, pval = test_hypo(list_card, list_cash, alpha=alpha, alternative='greater')
print()
print('t-Statistic Value: {}\nP-Value: {}'.format(t_stat, pval))
print()
# %%
# The average price of rides on week-days is lower than on weekends
# H0: Avg. price on week days = Avg. price on weekends
# Ha: Avg. price on week days < Avg. price on weekends
weekday_df = master[(master.day_name != 'Saturday') & (master.day_name != 'Sunday')]
weekend_df = master[(master.day_name == 'Saturday') | (master.day_name == 'Sunday')]
random_weekday = weekday_df.price.sample(n=1000)
random_weekend = weekend_df.price.sample(n=1000)
list_weekday = list(random_weekday.values)
list_weekend = list(random_weekend.values)
# %%
# Running the hypothesis test for test 5
hypothesis = 'The average price of rides on week-days is lower than on weekends'
null = 'Avg. price on week days = Avg. price on weekends'
alternate = 'Avg. price on week days < Avg. price on weekends'
disp(null, alternate, hypothesis)
for alpha in alphas:    
    t_stat, pval = test_hypo(list_weekday, list_weekend, alpha=alpha, alternative='less')
print()
print('t-Statistic Value: {}\nP-Value: {}'.format(t_stat, pval))
print()
# %%
# The average distance travelled by the Yellow cabs is greater than the the average distance travelled by the Pink cabs
# H0: Avg. distance travelled by Yellow Cabs = Avg. distance travelled by Pink Cabs
# Ha: Avg. distance travelled by Yellow Cabs > Avg. distance travelled by Pink Cabs
yellow_df = master[master.company == 'Yellow Cab']
pink_df = master[master.company == 'Pink Cab']
random_yellow = yellow_df.distance.sample(n=1000)
random_pink = pink_df.distance.sample(n=1000)
list_yellow = list(random_yellow.values)
list_pink = list(random_pink.values)
# %%
# Running the hypothesis test for test 6
hypothesis = 'The average distance travelled by the Yellow cabs is greater than the the average distance travelled by the Pink cabs'
null = 'Avg. distance travelled by Yellow Cabs = Avg. distance travelled by Pink Cabs'
alternate = 'Avg. distance travelled by Yellow Cabs > Avg. distance travelled by Pink Cabs'
disp(null, alternate, hypothesis)
for alpha in alphas:    
    t_stat, pval = test_hypo(list_yellow, list_pink, alpha=alpha, alternative='less')
print()
print('t-Statistic Value: {}\nP-Value: {}'.format(t_stat, pval))
print()
# %%

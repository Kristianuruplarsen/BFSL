
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from datetime import datetime
from datetime import timedelta

data = pd.read_csv('BFSL.csv', na_values = ['-'], dtype = {'supporters':str})

# convert supporters to string to remove the . and then back tu float
data['supporters'] = pd.to_numeric(data['supporters'].str.replace('.',''))

# ==============================================================================
# this section is all about getting the date variables to make sense
# ==============================================================================
month_abbreviations = {'januar': 1,
                       'februar': 2,
                       'marts': 3,
                       'april': 4,
                       'maj': 5,
                       'juni': 6,
                       'juli': 7,
                       'august': 8,
                       'september': 9,
                       'oktober': 10,
                       'november': 11,
                       'december': 12}

def match_month(month_string):
    try:
        return month_abbreviations[month_string]
    except:
        return np.NaN

# first lets expand the dates
data['day'] = data['start_date'].str.split('.', n = 1).apply(lambda x: int(x[0].strip()))
data['start_month'] = data['start_date'].str.split(' ').apply(lambda x: x[1])
data['year'] = data['start_date'].str.split(' ').apply(lambda x: x[2])
data['month'] = data['start_month'].apply(match_month)
data['start_date'] = pd.to_datetime(data[['year','month','day']], errors = 'coerce')

# this is kinda shady, but it serves the purpose and fixes a issue with subsetting lists when some cells are missing
data['day'] = data['end_date'].fillna('-1. ASD').str.split('.', n = 1).apply(lambda x: int(x[0]))
data['end_month'] = data['end_date'].fillna('ASD NaN ASD').str.split(' ').apply(lambda x: x[1])

data['day'].replace(-1, np.NaN, inplace = True)
data['end_month'].replace('NaN', np.NaN, inplace = True)

data['year'] = data['end_date'].fillna('ASD ASD NaN').str.split(' ').apply(lambda x: x[2])
data['month'] = data['end_month'].apply(match_month)

data['end_date'] = pd.to_datetime(data[['year','month','day']], errors = 'coerce')

# finally lets drop the unneeded variables
data.drop(['day', 'month','year'], axis = 1)


date = datetime.today()
today = pd.to_datetime('-'.join(map(str, [date.year, date.month, date.day])), format = '%Y-%m-%d')


def upper_time_limit(x):
    ''' Enforces the upper timedelta of 180 days for a suggestion
    '''
    if x > timedelta(180):
        return timedelta(180)
    else:
        return x

# running days
data['running_days'] = today - data['start_date']
data['running_days'] = data['running_days'].apply(upper_time_limit)

# length of main text
data['text_length'] = data['text'].apply(len)
# ==============================================================================
# this plots a bunch of kernel densities to get a first impression
# of the continous variables
# ==============================================================================

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, sharey = False, figsize= (10,5))

sns.kdeplot(data['start_date'].dt.day.dropna(), shade = True, cut = 1, color = 'r', ax = ax1)
ax1.set_title('Start day')
ax1.legend_.remove()

sns.kdeplot(data['running_days'].dt.days, shade = True, cut = 1, color = 'g', ax = ax2)
ax2.set_title('Running days')
ax2.legend_.remove()

sns.kdeplot(data['supporters'], shade = True, cut = 0, ax = ax3)
ax3.set_title('Supporter count')
ax3.legend_.remove()

fig.legend(['start date','Running days','Supporter count density'], loc = 'lower center', ncol = 3, bbox_to_anchor = (0.5, -.018))

plt.suptitle('Densities', fontsize = 20)
plt.tight_layout()
plt.subplots_adjust(top=0.85)
plt.savefig('figures/Densities.png')
plt.show()

# This is a jointplot of running days and
(sns.jointplot(data['running_days'].dt.days, data['supporters'], kind = 'kde', color = 'm', space = 0)
).set_axis_labels('Running days', 'Supporters')

plt.savefig('figures/Jointplot.png')
plt.show()



data.to_csv('BFSL_updated.csv')

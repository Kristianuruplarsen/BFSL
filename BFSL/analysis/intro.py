
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

data = pd.read_csv('BFSL.csv', na_values = ['-'])

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


# ==============================================================================
# this plots a bunch of kernel densities to get a first impression
# of the continous variables
# ==============================================================================

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, sharey = False, figsize= (10,5))

sns.kdeplot(data['start_date'].dt.day.dropna(), shade = True, cut = 1, color = 'r', ax = ax1)
ax1.set_title('Start day')
ax1.legend_.remove()

sns.kdeplot(data['end_date'].dt.day.dropna(), shade = True, cut = 1, color = 'g', ax = ax2)
ax2.set_title('End day')
ax2.legend_.remove()

sns.kdeplot(data['supporters'], shade = True, cut = 0, ax = ax3)
ax3.set_title('Supporter count')
ax3.legend_.remove()

fig.legend(['start date','end date','Supporter count density'], loc = 'lower center', ncol = 3, bbox_to_anchor = (0.5, -.02))

plt.suptitle('Densities', fontsize = 20)
plt.tight_layout()
plt.subplots_adjust(top=0.85)
plt.show()



# ==============================================================================
# Now lets start looking at the text data
# ==============================================================================

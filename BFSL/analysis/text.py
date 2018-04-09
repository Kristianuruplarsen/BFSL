
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from afinn import Afinn


data = pd.read_csv('BFSL_updated.csv', na_values = ['-'])

# quick and dirty sentiment scores
afinn = Afinn(language = 'da')

data['sentiment'] = data['text'].apply(afinn.score)
data['sentiment_to_length'] = data['sentiment'] / data['text_length']


# Ok first a very simple plot of the sentiment distribution
sns.kdeplot(data['sentiment'], shade = True, color = 'm')
plt.legend(['Sentiment'])
plt.title('Distribution of proposal sentiments')
plt.savefig('figures/Sentiment.png')
plt.show()

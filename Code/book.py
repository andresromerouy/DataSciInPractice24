## [UM-05E] Example - Book recommendations ##

# Importing the data #
import pandas as pd
path = 'https://raw.githubusercontent.com/mikecinnamon/DataSci/main/Data/'
ratings = pd.read_csv(path + 'book_ratings.csv.zip')
ratings.info()
items = pd.read_csv(path + 'book_items.csv.zip')
items.info()

# Joining the tables #
df = ratings.merge(items)
df.info()

# Q1. How often do bookcrossers rate the books they pick? #
(ratings['rating'] > 0).mean().round(3)

# Q2. Which titles have been picked more times? #
df['title'].value_counts().head(10)

# Q3. Which books have been rated highest? #
df1 = df[df['rating'] > 0][['title', 'rating']].groupby(by='title').agg(['mean', 'count'])
df1.head()
df1.columns
df1.columns= ['mean', 'count']
df1[df1['count'] >= 25].sort_values(by='mean', ascending=False).head(10)

# Q4. How many editions of The Martian Chronicles in English #
items[items['title'].str.contains('martian chronicles', case=False)]
mc_isbn = items[items['title'].str.contains('martian chronicles', case=False)]['isbn']
mc_isbn

# Q5a. How many users picking The Martian Chronicles #
mc_count = (df['isbn'].isin(mc_isbn)).sum()
mc_count

# Q5b. Selecting data for the recommendation #
mc_users = df[df['isbn'].isin(mc_isbn)]['user']
mc_df = df[df['user'].isin(mc_users)]
mc_df = mc_df[~mc_df['isbn'].isin(mc_isbn)]

# Q5c. Recommendation for readers of The Martian Chronicles #
conf = mc_df['isbn'].value_counts()/mc_count
conf
pd.DataFrame({'conf': conf}).join(items.set_index('isbn'))[['title', 'author', 'conf']]

# Q5d. Variation
mc_conf = pd.DataFrame({'conf': conf}).join(items.set_index('isbn'))[['title', 'author', 'conf']]
mc_conf.groupby(by=['title', 'author'])['conf'].sum().sort_values(ascending=False)[:5]

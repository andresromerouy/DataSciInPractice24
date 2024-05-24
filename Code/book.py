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

# Q5. Recommendation for readers of The Martian Chronicles #
mc_users = df[df['title'].str.contains('martian chronicles', case=False)]['user']
mc_users
mc_df = df[df['user'].isin(mc_users)]
mc_df = mc_df[~mc_df['title'].str.contains('martian chronicles', case=False)]
mc_df.shape
conf = mc_df['isbn'].value_counts()/len(mc_users)
conf
pd.DataFrame({'conf': conf[:5]}).merge(items, left_index=True, right_on='isbn')[['title', 'author', 'conf']]
mc_conf = pd.DataFrame({'conf': conf}).merge(items, left_index=True, right_on='isbn')[['title', 'author', 'conf']]
mc_conf.groupby(by=['title', 'author'])['conf'].sum().sort_values(ascending=False)[:5]

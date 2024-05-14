## [UM-01E1] Example - Apple Inc. stock prices ##

# Import the data #
import pandas as pd
path = 'https://raw.githubusercontent.com/mikecinnamon/DataSci/main/Data/'
df = pd.read_csv(path + 'aapl.csv')

# Exploring the data #
df.info()
df.head()
df.describe()

# Q1. Data previous to January 15th #
df[df['date'] < '2022-01-15']

# Q2. Line plot for the opening price #
df['open'].plot(figsize=(8,5), title='Figure 1. Opening price (USD)', color='black', linewidth=1);

Q3a. Line plot for the trading volume #
df['volume'] = df['volume']/10**6
df['volume'].plot(figsize=(8,5), title='Figure 2. Trading volume (million shares)', color='black', linewidth=1);

# Q3b. Histogram for the trading volume #
df['volume'].plot.hist(figsize=(7,5),
    title='Figure 3. Trading volume (alternative visualization)',
    color='gray', edgecolor='white', xlabel='Trading volume (million shares)');

# Q4a. Daily variation #
df['dvar'] = df['high'] - df['low']
df.head()

# Q4b. Line plot for the daily variation #
df['dvar'].plot(figsize=(8,5), title='Figure 4. Daily price variation (USD)',
    color='black', linewidth=1);

# Q4c. Histogram for the daily variation #
df['dvar'].plot.hist(figsize=(7,5),
    title='Figure 5. Daily price variation (alternative visualization)',
    color='gray', edgecolor='white', xlabel='Daily price variation (USD)');

# Q5a. Scatter plot for the daily price variation and the trading volume # 
df.plot.scatter(x='volume', y='dvar', 
    title='Figure 6. Daily variation vs volume', figsize=(5,5), color='gray',
    xlabel='Trading volume (million shares)', ylabel='Daily price variation (USD)');

## Q5b. Correlation #
df['volume'].corr(df['dvar'])
df['volume'].corr(df['dvar']).round(2)

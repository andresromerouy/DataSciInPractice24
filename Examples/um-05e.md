# [UM-05E] Example - Book recommendations

## Introduction

**Bookcrossing** is defined as *the practice of leaving a book in a public place to be picked up and read by others, who then do likewise*. The term is derived from BookCrossing (`bookcrossing.com`), a free online book club which was founded to encourage the practice, aiming to *make the whole world a library*.

The crossing or exchanging of books may take various forms, including wild-releasing books in public, direct swaps with other members of the websites, or *book rings* in which books travel in a specified order to participants who want to read a certain book. The community aspect of BookCrossing has grown and expanded in the form of blog or forum discussions, mailing lists and annual conventions throughout the world.

BookCrossing was launched on April 21, 2001. By November 2019, there were over 1.9 million members and over 13 million books traveling through 132 countries, of which over 25 thousand books newly "released in the wild" in the previous month across over 60 countries. Over 80% of the books were released in the eight most active countries (Germany, United States, Spain, Italy, Australia, United Kingdom, the Netherlands and Brasil). The world's first official International BookCrossing Day took place on April 21st, 2014.

Cai-Nicolas Zeigler collected over one million ratings of books from the BookCrossing website. Since the books are identified by the ISBN, what we call here a book is, really, an edition of a book. Popular books, such as *Harry Potter and the Sorcerer's Stone*, have several editions in this database. Individual users come mixed with book rings, so some of the users have a very high number of book pickings. Since these rings may also rate the books (with a single rating), they have not been removed. 

## The data set

The data for this example come in three tables. The file `book_users.csv` (zipped) contains information about 92,106 users. The columns are:

* `user`, the user's ID (anonymized).

* `location`, the user's location, as 'city, state, country'. Example: 'moscow, yukon territory, russia'.

* `age`, the user's age, in years. Almost 40% of the data are missing.

The file `book_items.csv` (zipped) contains information about 270,151 books on circulation. The columns are: 

* `isbn`, the ISBN code of the book, which works as the book ID. Invalid ISBN's have already been removed.

* `title`, the title of the book.

* `author`, the book's author, obtained from Amazon Web Services. In case of several authors, only the first one is provided. One value is missing.

* `year`, the year of publication, obtained from Amazon Web Services. 1.7% of the values are missing.

* `publisher`, the book's publisher, obtained from Amazon Web Services. Two values are missing.

* `image`, an URL linking to the cover image. These URL's point to the Amazon web site. Two values are missing.

The file `book_ratings.csv` (zipped) contains 1,031,136 ratings. The columns are:

* `user`, the user's ID.

* `isbn`, the books's ISBN.

* `rating`, either the rating given by the user (1-10 range) or 0, when the user did not provide a rating.

Source: C-N Ziegler, SM McNee, JA Konstan & G Lausen (2005), Improving Recommendation Lists Through Topic Diversification, in *Proceedings of the 14th International World Wide Web Conference*, Chiba, Japan. The inactive users have been dropped from the table `users`, and the unpicked books from `items`.

## Questions

Q1. How often do bookcrossers rate the books they pick?

Q2. Which titles have been picked more times?

Q3. Which books have been rated highest? 

Q4. How many editions of the SF classic *The Martian Chronicles* are offered by BookCrossing?

Q5. From the data provided, extract a list of five books to be recommended to users having picked *The Martian Chronicles*. A simple approach would be to search for the titles that have been picked more often by the users who have also picked *The Martian Chronicles*.

## Importing the data

We start by importing Pandas, as usual.

```
In [1]: import pandas as pd
```

The data consists of three tables. I import the table `ratings` from the GitHub repository as we have with other tables before:

```
In [2]: path = 'https://raw.githubusercontent.com/cinnData/DataSci/main/Data/'
```

```
In [3]: ratings = pd.read_csv(path + 'book_ratings.csv.zip')
   ...: ratings.info()
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 1031136 entries, 0 to 1031135
Data columns (total 3 columns):
 #   Column  Non-Null Count    Dtype 
---  ------  --------------    ----- 
 0   user    1031136 non-null  int64 
 1   isbn    1031136 non-null  object
 2   rating  1031136 non-null  int64 
dtypes: int64(2), object(1)
memory usage: 23.6+ MB
```

The same for the table `items`: 

```
In [4]: items = pd.read_csv(path + 'book_items.csv.zip')
   ...: items.info()
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 271360 entries, 0 to 271359
Data columns (total 6 columns):
 #   Column     Non-Null Count   Dtype  
---  ------     --------------   -----  
 0   isbn       271360 non-null  object 
 1   title      271360 non-null  object 
 2   author     271359 non-null  object 
 3   year       266742 non-null  float64
 4   publisher  271358 non-null  object 
 5   image      271357 non-null  object 
dtypes: float64(1), object(5)
memory usage: 12.4+ MB
```

We leave aside the table `users`, because it will not involved in the analysis of this example.

## Joining the tables

The Pandas function `merge()` joins two data frames based on common columns. The default of this function performs what in SQL is called a **natural join**, that is, it joins the tables based on the columns with the same name in both tables.

We join `ratings` with `items`. The join is based on the (common) column `isbn`. We call `df` the data frame resulting from this join. 

```
In [5]: df = ratings.merge(items)
   ...: df.info()
<class 'pandas.core.frame.DataFrame'>
Int64Index: 1031136 entries, 0 to 1031135
Data columns (total 8 columns):
 #   Column     Non-Null Count    Dtype  
---  ------     --------------    -----  
 0   user       1031136 non-null  int64  
 1   isbn       1031136 non-null  object 
 2   rating     1031136 non-null  int64  
 3   title      1031136 non-null  object 
 4   author     1031135 non-null  object 
 5   year       1017127 non-null  float64
 6   publisher  1031134 non-null  object 
 7   image      1031132 non-null  object 
dtypes: float64(1), int64(2), object(5)
memory usage: 70.8+ MB
```

## Q1. How often do bookcrossers rate the books they pick?

Compared to e-commerce sites like Amazon, rating in Bookcrossing is quite frequent, although more than one half of the books picked are not rated. The books effectively rated are those with positive rating, so we can use the Boolean mask `ratings['rating'] > 0` to capture them:

```
In [6]: (df['rating'] > 0).mean().round(3)
Out[6]: 0.372
```

## Q2. Which titles have been picked more times?

To see which titles have been picked more times, we apply the method `.value_counts()`:

```
In [7]: df['title'].value_counts().head(10)
Out[7]: 
Wild Animus                                        2502
The Lovely Bones: A Novel                          1295
The Da Vinci Code                                   898
A Painted House                                     838
The Nanny Diaries: A Novel                          828
Bridget Jones's Diary                               815
The Secret Life of Bees                             774
Divine Secrets of the Ya-Ya Sisterhood: A Novel     740
The Red Tent (Bestselling Backlist)                 723
Angels &amp; Demons                                 670
Name: title, dtype: int64
```

## Q3. Which books have been rated highest?

To calculate the average rating for the books of this collection, we first select the titles that have been rated by at least once with `df['rating'] > 0`. Then, we group the ratings by title and calculate the average rating. We add the number of observations to help us to set a minimum number of picks.

```
In [8]: df1 = df[df['rating'] > 0][['title', 'rating']].groupby(by='title').agg(['mean', 'count'])
   ...: df1.head()
Out[8]: 
                                                       rating      
                                                         mean count
title                                                              
 A Light in the Storm: The Civil War Diary of A...   9.000000     1
 Ask Lily (Young Women of Faith: Lily Series, B...   8.000000     1
 Dark Justice                                       10.000000     1
 Earth Prayers From around the World: 365 Praye...   7.142857     7
 Final Fantasy Anthology: Official Strategy Gui...  10.000000     2
```

The column names may look a bit strange to you. They are a multi-index object (Pandas sophistication). 

```
In [9]: df1.columns
Out[9]: 
MultiIndex([('rating',  'mean'),
            ('rating', 'count')],
           )
```

This can be simplified as follows.

```
In [10]: df1.columns= ['mean', 'count']
```

Some books in this collection are marginal, so we can restrict the selection to the titles that have been rated by a minimum number of users, say 25, and sort by the average rating:

```
df1[df1['count'] >= 25].sort_values(by='mean', ascending=False).head(10)
Out[11]: 
                                                        mean  count
title                                                              
The Giving Tree                                     9.423077     26
Where the Sidewalk Ends : Poems and Drawings        9.400000     25
The Two Towers (The Lord of the Rings, Part 2)      9.330882    136
The Cat in the Hat                                  9.242424     33
Weirdos From Another Planet!                        9.240000     25
The Return of the King (The Lord of the Rings, ...  9.213592    103
Lonesome Dove                                       9.162162     37
The Grapes of Wrath                                 9.129032     31
Harry Potter and the Goblet of Fire (Book 4)        9.125506    247
Roots                                               9.120000     25
```

## Q4. How many editions of *The Martian Chronicles* in English?

There may be several editions of the *The Martian Chronicles* in BookCrossing. Also, it may be tha the title is not always written in the same way. To allow for these variations, instead of `items['title'] == 'martian chronicles'`, we use the Pandas method `str.contains()`. Indeed, there are some editions with an incomplete title (in the database).  

```
In [12]: items[items['title'].str.contains('martian chronicles', case=False)]
Out[12]: 
              isbn                   title        author    year  \
175     0553278223  The Martian Chronicles  RAY BRADBURY  1984.0   
277     0380973839      Martian Chronicles  Ray Bradbury  1997.0   
15537   0553263633      Martian Chronicles  Ray Bradbury  1984.0   
59089   0553131796      Martian Chronicles  Ray Bradbury     NaN   
96297   0553229680      Martian Chronicles  Ray Bradbury  1982.0   
224916  0553246917      Martian Chronicles  Ray Bradbury  1982.0   

                    publisher  \
175                   Spectra   
277            William Morrow   
15537            Bantam Books   
59089   Bantam Doubleday Dell   
96297            Bantam Books   
224916           Bantam Books   

                                                    image  
175     http://images.amazon.com/images/P/0553278223.0...  
277     http://images.amazon.com/images/P/0380973839.0...  
15537   http://images.amazon.com/images/P/0553263633.0...  
59089   http://images.amazon.com/images/P/0553131796.0...  
96297   http://images.amazon.com/images/P/0553229680.0...  
224916  http://images.amazon.com/images/P/0553246917.0...  
```

We prepare aside a list of the ISBN's of these six editions. This would be `mc_isbn`.

```
In [13]: mc_isbn = items[items['title'].str.contains('martian chronicles', case=False)]['isbn']
    ...: mc_isbn
Out[13]: 
175       0553278223
277       0380973839
15537     0553263633
59089     0553131796
96297     0553229680
224916    0553246917
Name: isbn, dtype: object
```

## Q5. Five books to be recommended to users having picked *The Martian Chronicles*

For further calculations, we retain the number of times The Martian Chronicles has been picked. This woul be `mc_count`, which turns out to be 93.

```
In [14]: mc_count = (df['isbn'].isin(mc_isbn)).sum()
    ...: mc_count
Out[14]: 93
```
The recommendation will involve books that been picked by the users that have picked Users who have picked *The Martian Chronicles*. This would be `mc_users`.

```
In [15]: mc_users = df[df['isbn'].isin(mc_isbn)]['user']
```

*Note*. You may easily check (with `.value_counts()`) that two users picked twice this book, so there are only 91 unique users in `mc_users`. But this would not affect our recommendation, so our code ignore ignore it.

The data used for the recommendation will be those involving the selected users. This would be `mc_df`

```
In [16]: mc_df = df[df['user'].isin(mc_users)]
```

Every row corresponds to one book picked by the selected users. We don't want to include *The Martian Chronicles* among the recommended books, so we drop the corresponding rows.

```
In [17]: mc_df = mc_df[~mc_df['isbn'].isin(mc_isbn)]
```

The recommended books will be thos appearing more often in `mc_df`. I can express this in relative terms as the **confidence**

```
In [18]: conf = mc_df['isbn'].value_counts()/mc_count
    ...: conf
Out[18]: 
0345342968    0.301075
0971880107    0.279570
044021145X    0.268817
0449212602    0.258065
0316666343    0.247312
                ...   
3570006360    0.010753
3570003167    0.010753
3552052054    0.010753
3552048693    0.010753
1583330844    0.010753
Name: isbn, Length: 41479, dtype: float64
```

The interpretation of the confidence is straightforward: on top, 30.1% of the readers of the *The Martian Chronicles* have picked the book with ISBN 0345342968. Next, 27.9% have picked the book with ISBN 0971880107. These would be the first recommendations.

```
In [19]: pd.DataFrame({'conf': conf[:5]}).join(items.set_index('isbn'))[['title', 'author', 'conf']]
Out[19]: 
                                title           author      conf
0345342968             Fahrenheit 451     RAY BRADBURY  0.301075
0971880107                Wild Animus     Rich Shapero  0.279570
044021145X                   The Firm     John Grisham  0.268817
0449212602        The Handmaid's Tale  Margaret Atwood  0.258065
0316666343  The Lovely Bones: A Novel     Alice Sebold  0.247312
```

Nevertheless, this is not a selection of titles, but a selection of ISBN's. You may wish to aggregate the editions, so your recommendation would be based on the title, and a later search would find the most accesible edition. This can be achieved by summing the confidences of the editions of the same title.

```
In [20]: mc_conf = pd.DataFrame({'conf': conf}).join(items.set_index('isbn'))[['title', 'author', 'conf']]
    ...: mc_conf.groupby(by=['title', 'author'])['conf'].sum().sort_values(ascending=False)[:5]
Out[20]: 
title                  author         
Fahrenheit 451         RAY BRADBURY       0.333333
The Handmaid's Tale    Margaret Atwood    0.301075
To Kill a Mockingbird  Harper Lee         0.290323
The Firm               John Grisham       0.279570
Wild Animus            Rich Shapero       0.279570
Name: conf, dtype: float64
```

What happened? *Wild Animus* has only one edition, while the other competitors have several editions. How does the recommendation work? If you pick one of the editions of the *The Martian Chronicles* in English, the titles *Farenheit 451*, *The Handmaid's Tale*, etc will be recommended, in the order displayed in `Out[20]`.

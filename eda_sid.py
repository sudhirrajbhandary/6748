import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings('ignore')

#print display
pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)

#main imdb file
path = 'data/Imdb Movie Dataset.csv'
data = pd.read_csv(path) #reads data

#filter and calculations
movies_revenue = data.loc[(data['budget'] > 0) & (data['revenue']  > 0)]
movies_revenue['profit'] = movies_revenue['revenue'] > movies_revenue['budget']
movies_revenue['budget_millions'] = round(movies_revenue['budget']/1000000,2)
movies_revenue['revenue_millions'] = round(movies_revenue['revenue']/1000000,2)

#genres into categorical variables
df_column = pd.get_dummies(movies_revenue['genres'].str.split(',\s*').explode()).groupby(level=0).sum()
movies_revenue = pd.concat([movies_revenue, df_column], axis=1)

#save genres into file
'''
df_column_sums = df_column.sum().T
path_out = 'data/genres.csv'
df_column_sums.sort_values(ascending=False).to_csv(path_out, index=True)
'''

#select production companies into categorical variables
#rest into other
allowed_production_companies = ['Warner Bros. Pictures',
                                'Universal Pictures',
                                'Paramount',
                                '20th Century Fox',
                                'Columbia Pictures',
                                'Metro-Goldwyn-Mayer',
                                'New Line Cinema',
                                'Walt Disney Pictures']

#split production companies
#explode into one row per production company
#only keep allowed production companies
#replace rest with 'other'
df_column = (movies_revenue['production_companies'].str.split(',\s*').explode()
             .apply(lambda x: x if x in allowed_production_companies else 'other'))

#remove duplicate 'other' production companies on same movie
df_column = df_column.to_frame()
df_column['id']=df_column.index
df_column = df_column.drop_duplicates()
df_column['id']=df_column.index
df_column = df_column.drop('id', axis=1)

#convert production companies to categorical columns
df_column = pd.get_dummies(df_column)
df_column = df_column.groupby(level=0).sum()

movies_revenue = pd.concat([movies_revenue, df_column], axis=1)

#save production companies into file
'''
df_column_sums = df_column.sum().T
path_out = 'data/production_companies.csv'
df_column_sums.sort_values(ascending=False).to_csv(path_out, index=True)
'''

#production_countries

#load lookup country continent file
path_country_continent = 'data/production_countries_continents.csv'
lookup_country_continent = pd.read_csv(path_country_continent) #reads data

#split and explode production countries column into multiple rows
#lookup 'Mapped Value' locations from file
df_column = movies_revenue['production_countries'].str.split(',\s*').explode()
df_column = df_column.to_frame()
df_column['id']=df_column.index
df_column = pd.merge(df_column, lookup_country_continent, left_on='production_countries', right_on='Country', how='left')

#remove duplicate 'Mapped Value' locations on same movie
df_column = df_column[['id','Mapped Value']]
df_column = df_column.drop_duplicates()

df_column = pd.get_dummies(df_column)
df_column.index=df_column['id']
df_column = df_column.groupby(level=0).sum()
df_column = df_column.drop('id', axis=1)
movies_revenue = pd.concat([movies_revenue, df_column], axis=1)

#runtimeminutes

#load lookup runtime file
path_runtime = 'data/title.basics.tsv'
lookup_runtime = pd.read_csv(path_runtime, sep='\t') #reads data
lookup_runtime = lookup_runtime[['tconst','runtimeMinutes']]

movies_revenue = pd.merge(movies_revenue, lookup_runtime, left_on='imdb_id', right_on='tconst', how='left')
movies_revenue = movies_revenue.drop('tconst', axis=1)

print(movies_revenue.shape)

path_out = 'data/output.csv'
movies_revenue.to_csv(path_out, index=False)


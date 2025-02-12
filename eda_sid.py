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

#languages
allowed_languages = ['English','Spanish','French']

#split languages
#explode into one row per languages
#only keep allowed languages
#replace rest with 'other'
df_column = (movies_revenue['spoken_languages'].str.split(',\s*').explode()
             .apply(lambda x: x if x in allowed_languages else 'other'))

#remove duplicate 'other' languages on same movie
df_column = df_column.to_frame()
df_column['id']=df_column.index
df_column = df_column.drop_duplicates()
df_column['id']=df_column.index
df_column = df_column.drop('id', axis=1)

#convert languages to categorical columns
df_column = pd.get_dummies(df_column)
df_column = df_column.groupby(level=0).sum()

movies_revenue = pd.concat([movies_revenue, df_column], axis=1)

#save languages into file
'''
df_column_sums = df_column.sum().T
path_out = 'data/spoken_languages.csv'
df_column_sums.sort_values(ascending=False).to_csv(path_out, index=True)
'''

'''
#runtimeminutes

#load lookup runtime file
path_runtime = 'data/title.basics.tsv'
lookup_runtime = pd.read_csv(path_runtime, sep='\t') #reads data
lookup_runtime = lookup_runtime[['tconst','runtimeMinutes']]

movies_revenue = pd.merge(movies_revenue, lookup_runtime, left_on='imdb_id', right_on='tconst', how='left')
movies_revenue = movies_revenue.drop('tconst', axis=1)
'''

#get director and crew
path_crew = 'data/title.crew.tsv'
data_crew = pd.read_csv(path_crew, sep='\t') #reads data

movies_revenue = pd.merge(movies_revenue, data_crew, left_on='imdb_id', right_on='tconst', how='left')
movies_revenue = movies_revenue.drop('tconst', axis=1)

movies_revenue[['director1', 'director2', 'director_remaining']] = movies_revenue['directors'].str.split(',', n=2, expand=True)

path_name = 'data/name.basics.tsv'
data_name = pd.read_csv(path_name, sep='\t') #reads data

movies_revenue = pd.merge(movies_revenue, data_name, left_on='director1', right_on='nconst', how='left')
#movies_revenue = movies_revenue.drop('nconst', axis=1)
movies_revenue = movies_revenue.drop(columns=['nconst','birthYear','deathYear','primaryProfession','knownForTitles'], axis=1)
movies_revenue.rename(columns={'primaryName': 'dir1Name'}, inplace=True)

#print(movies_revenue.head(5))

movies_revenue = pd.merge(movies_revenue, data_name, left_on='director2', right_on='nconst', how='left')
movies_revenue = movies_revenue.drop(columns=['nconst','birthYear','deathYear','primaryProfession','knownForTitles'], axis=1)
movies_revenue.rename(columns={'primaryName': 'dir2Name'}, inplace=True)
#print(movies_revenue.head(5))

#movies_revenue[['actor1', 'actor2', 'actor3','actor_remaining]] = movies_revenue['directors'].str.split(',', n=2, expand=True)

path_out = 'data/output.csv'
movies_revenue.to_csv(path_out, index=False)



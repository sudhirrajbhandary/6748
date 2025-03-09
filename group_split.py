import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings('ignore')

#print display
pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)

#main imdb file
path = 'data/FinalInputData.csv'
data = pd.read_csv(path) #reads data
groupdata = data.iloc[:,24:67]
groupdata['success_level']=data['success_level']
result = groupdata.groupby('success_level').sum()

#path_out = 'data/sum.csv'
#result.to_csv(path_out, index=True)

#plot genres stacked absolute
plot_genres=result.iloc[:,0:19]
plot_genres=plot_genres.T
plot_genres_percent=plot_genres
plot_genres=plot_genres.reset_index()
plot_genres=plot_genres[['index','Flop','Success','Blockbuster']]

#print(plot_genres)
plot_genres.plot(x='index', kind='bar', stacked=True, title='Success Level By Genre')

#format plot
current_values = plt.gca().get_yticks()
plt.gca().set_yticklabels(['{:,}'.format(int(x)) for x in current_values])
plt.xlabel('Genre')
plt.ylabel('Number of Movies')
plt.tight_layout()
plt.show()

#plot genres stacked out of 100%
plot_genres_percent=plot_genres_percent[['Flop', 'Success', 'Blockbuster']].div(plot_genres_percent[['Flop', 'Success', 'Blockbuster']].sum(axis=1), axis=0) * 100
plot_genres_percent=plot_genres_percent.reset_index()
plot_genres_percent.plot(x='index', kind='bar', stacked=True, title='Success Level By Genre')

#format
current_values = plt.gca().get_yticks()
plt.gca().set_yticklabels(['{:,}'.format(int(x)) for x in current_values])
plt.xlabel('Genre')
plt.ylabel('Number of Movies %')
plt.tight_layout()
plt.show()

#plot production_companies
plot_production_companies=result.iloc[:,19:27]
plot_production_companies=plot_production_companies.T
plot_production_companies_percent=plot_production_companies
plot_production_companies=plot_production_companies.reset_index()
plot_production_companies=plot_production_companies[['index','Flop','Success','Blockbuster']]
plot_production_companies['index']=plot_production_companies['index'].str.slice(21)
plot_production_companies.plot(x='index', kind='bar', stacked=True, title='Success Level By Production Company')

#format plot
current_values = plt.gca().get_yticks()
plt.gca().set_yticklabels(['{:,}'.format(int(x)) for x in current_values])
plt.xlabel('Production Companies')
plt.ylabel('Number of Movies')
plt.tight_layout()
plt.show()

#plot genres stacked out of 100%
plot_production_companies_percent=plot_production_companies_percent[['Flop', 'Success', 'Blockbuster']].div(plot_production_companies_percent[['Flop', 'Success', 'Blockbuster']].sum(axis=1), axis=0) * 100
plot_production_companies_percent=plot_production_companies_percent.reset_index()
plot_production_companies_percent['index']=plot_production_companies_percent['index'].str.slice(21)
plot_production_companies_percent.plot(x='index', kind='bar', stacked=True, title='Success Level By Production Company')

#format plot
current_values = plt.gca().get_yticks()
plt.gca().set_yticklabels(['{:,}'.format(int(x)) for x in current_values])
plt.xlabel('Production Companies')
plt.ylabel('Number of Movies %')
plt.tight_layout()
plt.show()

#plot location
#print(result)
plot_location=result.iloc[:,28:39]
plot_location=plot_location.T
plot_location_percentage=plot_location
plot_location=plot_location.reset_index()
plot_location=plot_location[['index','Flop','Success','Blockbuster']]
plot_location['index']=plot_location['index'].str.slice(13)
plot_location.plot(x='index', kind='bar', stacked=True, title='Success Level By Production Location')

#format plot
current_values = plt.gca().get_yticks()
plt.gca().set_yticklabels(['{:,}'.format(int(x)) for x in current_values])
plt.xlabel('Production Location')
plt.ylabel('Number of Movies')
plt.tight_layout()
plt.show()

#plot genres stacked out of 100%
plot_location_percentage=plot_location_percentage[['Flop', 'Success', 'Blockbuster']].div(plot_location_percentage[['Flop', 'Success', 'Blockbuster']].sum(axis=1), axis=0) * 100
plot_location_percentage=plot_location_percentage.reset_index()
plot_location_percentage['index']=plot_location_percentage['index'].str.slice(13)
plot_location_percentage.plot(x='index', kind='bar', stacked=True, title='Success Level By Production Location')

#format plot
current_values = plt.gca().get_yticks()
plt.gca().set_yticklabels(['{:,}'.format(int(x)) for x in current_values])
plt.xlabel('Production Location')
plt.ylabel('Number of Movies %')
plt.tight_layout()
plt.show()

'''
**********8
'''
#plot location
plot_language=result.iloc[:,39:43]
#print(plot_language)

plot_language=plot_language.T
plot_language_percentage=plot_language
plot_language=plot_language.reset_index()
plot_language=plot_language[['index','Flop','Success','Blockbuster']]
plot_language['index']=plot_language['index'].str.slice(17)
plot_language.plot(x='index', kind='bar', stacked=True, title='Success Level By Production Language')

#format plot
current_values = plt.gca().get_yticks()
plt.gca().set_yticklabels(['{:,}'.format(int(x)) for x in current_values])
plt.xlabel('Production Language')
plt.ylabel('Number of Movies')
plt.tight_layout()
plt.show()

#plot genres stacked out of 100%
plot_language_percentage=plot_language_percentage[['Flop', 'Success', 'Blockbuster']].div(plot_language_percentage[['Flop', 'Success', 'Blockbuster']].sum(axis=1), axis=0) * 100
plot_language_percentage=plot_language_percentage.reset_index()
plot_language_percentage['index']=plot_language_percentage['index'].str.slice(17)
plot_language_percentage.plot(x='index', kind='bar', stacked=True, title='Success Level By Production Language')

#format plot
current_values = plt.gca().get_yticks()
plt.gca().set_yticklabels(['{:,}'.format(int(x)) for x in current_values])
plt.xlabel('Production Language')
plt.ylabel('Number of Movies %')
plt.tight_layout()
plt.show()

data = pd.read_csv(path) #reads data

from sklearn.model_selection import train_test_split
train_df, temp_df = train_test_split(data, test_size=0.3) # 80% train, 20% test
test_df, validation_df = train_test_split(temp_df, test_size=0.5) # 50% test, 50% validation

grouped_director = train_df.groupby('director1').size()
grouped_director_blockbuster = train_df[train_df['success_level']=='Blockbuster'].groupby('director1').size()
grouped_director_success = train_df[train_df['success_level']=='Success'].groupby('director1').size()
grouped_director_flop = train_df[train_df['success_level']=='Flop'].groupby('director1').size()

grouped_director=grouped_director.to_frame()
grouped_director=grouped_director.reset_index()
grouped_director.columns=['director1','dir_total']

grouped_director_blockbuster=grouped_director_blockbuster.to_frame()
grouped_director_blockbuster=grouped_director_blockbuster.reset_index()
grouped_director_blockbuster.columns=['director1','dir_blockbuster']

grouped_director_success=grouped_director_success.to_frame()
grouped_director_success=grouped_director_success.reset_index()
grouped_director_success.columns=['director1','dir_success']

grouped_director_flop=grouped_director_flop.to_frame()
grouped_director_flop=grouped_director_flop.reset_index()
grouped_director_flop.columns=['director1','dir_flop']

grouped_director = pd.merge(grouped_director,grouped_director_blockbuster, on='director1', how='left')
grouped_director = pd.merge(grouped_director,grouped_director_success, on='director1', how='left')
grouped_director = pd.merge(grouped_director,grouped_director_flop, on='director1', how='left')
#print(grouped_director)

train_actor_df = train_df.copy()
train_actor_df['actor1Name']=train_actor_df['actor2Name']
train_actor_df = train_actor_df._append(train_df.copy())

grouped_actor = train_actor_df.groupby('actor1Name').size()
grouped_actor_blockbuster = train_df[train_df['success_level']=='Blockbuster'].groupby('actor1Name').size()
grouped_actor_success = train_df[train_df['success_level']=='Success'].groupby('actor1Name').size()
grouped_actor_flop = train_df[train_df['success_level']=='Flop'].groupby('actor1Name').size()

grouped_actor=grouped_actor.to_frame()
grouped_actor=grouped_actor.reset_index()
grouped_actor.columns=['actor1Name','actor_total']

grouped_actor_blockbuster=grouped_actor_blockbuster.to_frame()
grouped_actor_blockbuster=grouped_actor_blockbuster.reset_index()
grouped_actor_blockbuster.columns=['actor1Name','actor_blockbuster']

grouped_actor_success=grouped_actor_success.to_frame()
grouped_actor_success=grouped_actor_success.reset_index()
grouped_actor_success.columns=['actor1Name','actor_success']

grouped_actor_flop=grouped_actor_flop.to_frame()
grouped_actor_flop=grouped_actor_flop.reset_index()
grouped_actor_flop.columns=['actor1Name','actor_flop']

grouped_actor = pd.merge(grouped_actor,grouped_actor_blockbuster, on='actor1Name', how='left')
grouped_actor = pd.merge(grouped_actor,grouped_actor_success, on='actor1Name', how='left')
grouped_actor = pd.merge(grouped_actor,grouped_actor_flop, on='actor1Name', how='left')
#print(grouped_actor)

train_actor_df['director1_actor1Name']=train_actor_df['director1']+'_'+train_actor_df['actor1Name']
grouped_director_actor = train_actor_df.groupby('director1_actor1Name').size()
grouped_director_actor_blockbuster = train_actor_df[train_actor_df['success_level']=='Blockbuster'].groupby('director1_actor1Name').size()
grouped_director_actor_success = train_actor_df[train_actor_df['success_level']=='Success'].groupby('director1_actor1Name').size()
grouped_director_actor_flop = train_actor_df[train_actor_df['success_level']=='Flop'].groupby('director1_actor1Name').size()

grouped_director_actor=grouped_director_actor.to_frame()
grouped_director_actor=grouped_director_actor.reset_index()
grouped_director_actor.columns=['director1_actor1Name','dir_act_total']

grouped_director_actor_blockbuster=grouped_director_actor_blockbuster.to_frame()
grouped_director_actor_blockbuster=grouped_director_actor_blockbuster.reset_index()
grouped_director_actor_blockbuster.columns=['director1_actor1Name','dir_act_blockbuster']

grouped_director_actor_success=grouped_director_actor_success.to_frame()
grouped_director_actor_success=grouped_director_actor_success.reset_index()
grouped_director_actor_success.columns=['director1_actor1Name','dir_act_success']

grouped_director_actor_flop=grouped_director_actor_flop.to_frame()
grouped_director_actor_flop=grouped_director_actor_flop.reset_index()
grouped_director_actor_flop.columns=['director1_actor1Name','dir_act_flop']

grouped_director_actor = pd.merge(grouped_director_actor,grouped_director_actor_blockbuster, on='director1_actor1Name', how='left')
grouped_director_actor = pd.merge(grouped_director_actor,grouped_director_actor_success, on='director1_actor1Name', how='left')
grouped_director_actor = pd.merge(grouped_director_actor,grouped_director_actor_flop, on='director1_actor1Name', how='left')
print(grouped_director_actor)

train_df['director1_actor1Name']=train_df['director1'] + '_' + train_df['actor1Name']
train_df = pd.merge(train_df, grouped_director, on='director1', how='left')
train_df = pd.merge(train_df, grouped_actor, on='actor1Name', how='left')
train_df = pd.merge(train_df, grouped_director_actor, on='director1_actor1Name', how='left')

path_out_dir_act = 'data/dir_act_df.csv'
grouped_director_actor.to_csv(path_out_dir_act, index=True)

path_out_train = 'data/train_df.csv'
train_df.to_csv(path_out_train, index=True)

test_df['director1_actor1Name']=test_df['director1'] + '_' + test_df['actor1Name']
test_df = pd.merge(test_df, grouped_director, on='director1', how='left')
test_df = pd.merge(test_df, grouped_actor, on='actor1Name', how='left')
test_df = pd.merge(test_df, grouped_director_actor, on='director1_actor1Name', how='left')

path_out_test = 'data/test_df.csv'
test_df.to_csv(path_out_test, index=True)

validation_df['director1_actor1Name']=validation_df['director1'] + '_' + validation_df['actor1Name']
validation_df = pd.merge(validation_df, grouped_director, on='director1', how='left')
validation_df = pd.merge(validation_df, grouped_actor, on='actor1Name', how='left')
validation_df = pd.merge(validation_df, grouped_director_actor, on='director1_actor1Name', how='left')

path_out_validation = 'data/validation_df.csv'
validation_df.to_csv(path_out_validation, index=True)


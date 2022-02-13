# Importing the packages that will be needed

import os
import numpy as np
import pandas as pd
from functools import reduce
import matplotlib.pyplot as plt
import seaborn as sns




# Moving to the current directory and checking the contents

wd = os.getcwd()
os.listdir(wd)




# Importing the datasets which are .csv files into pandas dataframes produced 
# a low memory and UnicodeDecodeError so the additional arguments of 
# 'low_memory = False' and encoding = 'latin-1' were included

# Dataset imports:

characteristics = pd.read_csv('caracteristics.csv', low_memory = False, 
                              encoding = 'latin-1')
holidays = pd.read_csv('holidays.csv', low_memory = False, 
                       encoding = 'latin-1')
places = pd.read_csv('places.csv', low_memory = False, 
                     encoding = 'latin-1')
users = pd.read_csv('users.csv', low_memory = False, 
                    encoding = 'latin-1')
vehicles = pd.read_csv('vehicles.csv', low_memory = False, 
                       encoding = 'latin-1')

# Converting to dataframes:

characteristics_df = pd.DataFrame(data = characteristics, index = None)
holidays_df = pd.DataFrame(data = holidays, index = None)
places_df = pd.DataFrame(data = places, index = None)
users_df = pd.DataFrame(data = users, index = None)
vehicles_df = pd.DataFrame(data = vehicles, index = None)

# Taking a look at the data:

df_list = (characteristics_df, holidays_df, places_df, users_df, vehicles_df)
for df in df_list:
    print(df.head())

# For my purposes I can do without the holidays_df dataframe.




# Next I want to see what the obvious differences are and that should be
# the length - i.e. do they all contain the same number of rows?

print(characteristics_df.shape,
      places_df.shape,
      users_df.shape,
      vehicles_df.shape)




# The datasets are all of different lengths so so firstly I'll take a look at
# the headings to see if there are any that may be a good candidate being the
# primary key. I'm going find this by combining the columns headers in each
# dataframe and creating a combined array. Then I'll be able to quickly pull 
# out which heading(s) is common to all - i.e. had more than 4 occurrences -
# 1 in each of the 4 dataframes.

df_headers_1_2 = np.append(characteristics_df.columns.values, 
                           places_df.columns.values)

# np.append can only take a maximum of 3 arguments whereas there's 4 dataframes

df_headers_3_4 = np.append(users_df.columns.values,
                           vehicles_df.columns.values)


all_df_headers = np.append(df_headers_1_2, df_headers_3_4)


common_headers = []
all_df_headers_list = list(all_df_headers)
for header in all_df_headers:
    if all_df_headers_list.count(header) == 4:
        if header not in common_headers:
            common_headers.append(header)
    else:
        pass
print(common_headers)

# 'Num_Acc' is common to all of the datasets. 




# Now we'll briefly look at the headings of each of the dataframes and see
# what data to pull out. I'll then create new dataframes with just the columns
# that will be usable for my purposes.

# Starting in order imported:

print(characteristics_df.columns.values)
print(places_df.columns.values)
print(users_df.columns.values)
print(vehicles_df.columns.values)


characteristics_df_selected_columns = characteristics_df[['Num_Acc', 'an', 
'mois', 'jour', 'hrmn', 'lum', 'atm', 'agg', 'col']]
# 'agg' is the correct heading, not 'localisation' as per Kaggle notes.
places_df_selected_columns = places_df[['Num_Acc','catr', 'plan', 
 'surf', 'situ']]
users_df_selected_columns = users_df[['Num_Acc', 'catu', 'grav', 'sexe',
'an_nais', 'trajet', 'secu']]
vehicles_df_selected_columns = vehicles_df[['Num_Acc', 'catv']]




# Joining the four datasets to create one useable dataset:

all_df_selected_columns = [characteristics_df_selected_columns,
                           places_df_selected_columns,
                           users_df_selected_columns,
                           vehicles_df_selected_columns]

combined_df = reduce(lambda left,right: pd.merge(left,right,on='Num_Acc'), 
                   all_df_selected_columns)

print(combined_df.columns.values)   # The headings are all there
print(combined_df.head())           # The data looks to be correct




# Renaming the headings to make them more user-friendly:

combined_df_headings = [str(heading) for heading in combined_df.columns.values]

new_headings = ['Num_Acc', 'year', 'month', 'day', 'time', 'lighting',
                'atmos_conditions', 'localisation', 'collision_type', 
                'road_cat', 'road_shape', 'surface', 'situation', 'user_cat',
                'severity', 'sex', 'dob', 'reason', 'safety_equip',
                'vehicle_cat']


headings_dict = dict(zip(combined_df_headings, new_headings))
print(headings_dict)


master_df = combined_df.rename(headings_dict, axis = 1)
print(master_df.columns.values)
print(master_df.head())




# Now that we have the master dataset, we'll do some exploration & cleaning:

# defining a function to change the 'year' values to 2000's

def add_millennium(year):
    return year + 2000

master_df['year'] = master_df['year'].apply(add_millennium)

# creating an age column from the 'year' and 'dob'

master_df['age'] = master_df['year'] - master_df['dob']
print(master_df[['year', 'dob', 'age']])

# creating a count column for the number of accidents - dividing the 'year' by
# itself as missing data should throw up an error - note, this may not be used

master_df['acc_count'] = master_df['year'] / master_df['year']
print(master_df['acc_count'].isnull().sum())   # no misssing data
print(master_df.groupby('year').count())
print(master_df['acc_count'])

# splitting out the 'safety_equip' column into type and whether used or not:

master_df['safety_equip'].unique()
master_df['safety_equip'].fillna(0, inplace = True)
print(master_df['safety_equip'].unique())


master_df['safety_equip_type'] = master_df['safety_equip'] / 10 # to be able to index
master_df['safety_equip_type'] = master_df['safety_equip_type'].astype('string')


def type_split(column):
    return column[0]

master_df['safety_equip_type'] = master_df['safety_equip_type'].apply(type_split)
print(master_df['safety_equip_type'].head())


master_df['safety_equip_type'] = master_df['safety_equip_type'].\
    replace({"1": "Belt", "2": "Helmet", "3": "Children's Device",
             "4": "Reflective Equipment", "9": "Other"})
    
print(master_df['safety_equip_type'].head())



master_df['safety_equip_used'] = master_df['safety_equip'] / 10 # to be able to index
master_df['safety_equip_used'] = master_df['safety_equip_used'].astype('string')

def use_split(column):
    return column[-1]

master_df['safety_equip_used'] = master_df['safety_equip_used'].apply(use_split)
print(master_df['safety_equip_used'].head())

master_df['safety_equip_used'] = master_df['safety_equip_used'].\
    replace({"1": "Yes", "2": "No", "3": "Not Determinable"})
    
print(master_df['safety_equip_used'].head())


#master_df['safety_equip_type'] = master_df['safety_equip'].str.split('.')
#print(master_df['safety_equip_type'].dtypes)
#master_df['safety_equip_type'] = master_df['safety_equip_type'].str.split(n = 0, expand = False).str[0]
#print(master_df['safety_equip_type'].head())

#master_df['safety_equip_used'] = master_df['safety_equip_type'].astype(str)

#print(master_df[['safety_equip','safety_equip_type', 'safety_equip_used']].head())



#master_df['safety_equip_type'] = master_df['safety_equip_type'].str(:-2).astype(float)

# Removing duplicates:

#duplications = master_df.duplicated()
#print(duplications.value_counts())
#master_df = master_df.drop_duplicates()

#duplications = master_df.duplicated()
#print(duplications.value_counts())       # the True's have been removed




# CHARTS



#print(master_df.info(null_counts = True))
#print(master_df.isnull().sum())
#null_list = master_df.columns[master_df.isnull().any()].tolist()


#print(master_df.describe())
#print(master_df.values)
#print(master_df.columns)
#print(master_df.index)




# Visualizing the data:





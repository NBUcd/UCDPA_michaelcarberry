# Importing the packages that will be needed

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn
import os


# Moving to the current directory and checking the contents

wd = os.getcwd()
os.listdir(wd)


# Importing the datasets which are .csv files into pandas dataframes produced 
# a UnicodeDecodeError so the additional argument of encoding='latin-1' was
# included


characteristics = pd.read_csv('caracteristics.csv', encoding='latin-1')
holidays = pd.read_csv('holidays.csv', encoding='latin-1')
places = pd.read_csv('places.csv', encoding='latin-1')
users = pd.read_csv('users.csv', encoding='latin-1')
vehicles = pd.read_csv('vehicles.csv', encoding='latin-1')

characteristics_df = pd.DataFrame(data = characteristics, index = None)
holidays_df = pd.DataFrame(data = holidays, index = None)
places_df = pd.DataFrame(data = places, index = None)
users_df = pd.DataFrame(data = users, index = None)
vehicles_df = pd.DataFrame(data = vehicles, index = None)


# Firstly I want to see what the obvious differences are and that should be
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



#print(characteristics_df.info())
#print(characteristics_df.describe())

#print(characteristics_df.values)
#print(characteristics_df.columns)
#print(characteristics_df.index)



# To make the datasets easier to use, I'll change the more obviously useful
# headings from French to English
# To do this, I'll create a single list (as a numpy array) of the headers 
# with duplicates removed and look up against a dictionary containing the 
# English translation.
# then I'll iterate through all of the headings in the individual dataframes 
# to replace them with their English translation

#df_headers_1_2 = np.append(characteristics_df.columns.values, 
#                           places_df.columns.values)

# np.append can only take a maximum of 3 arguments whereas there's 4 dataframes

#df_headers_3_4 = np.append(users_df.columns.values,
#                           vehicles_df.columns.values)

#all_df_headers = np.append(df_headers_1_2, df_headers_3_4)

#unique_df_headers = np.unique(all_df_headers)

#df_headers_to_translate = ['an', 'mois', 'jour', 'hrmn', 'lum', 'voie', 'circ', 
#                        'grav', 'Year_on']

#translation = {'an':'year', 'mois':'month', 'jour':'day', 'hrmn':'time', 
#               'lum':'lighting', 'voie':'road_number', 
#               'circ':'traffic_regime', 'grav':'severity', 'Year_on':'DOB'}


#for header in users_df.columns.values:
#    if header in df_headers_to_translate:
#        print(translation[header])
#    else:
#        print('not in list')

#for header in users_df.columns.values:
#    if header in df_headers_to_translate:
#        users_df.rename({header:translation[header]})
#    else:
#        pass
    
#print(users_df.head())



#print(all_df_headers)
#print(users_df['secu'])
#print(df_headers_to_translate)


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


# To make the datasets easier to use, I'll change the more obviously useful
# headings from French to English
# To do this, I'll create a single list (as a numpy array) of the headers 
# with duplicates removed and look up against a dictionary containing the 
# English translation.
# then I'll iterate through all of the headings in the individual dataframes 
# to replace them with their English translation

df_headers_1_2 = np.append(characteristics_df.columns.values, 
                           places_df.columns.values)

# np.append can only take a maximum of 3 arguments whereas there's 4 dataframes

df_headers_3_4 = np.append(users_df.columns.values,
                           vehicles_df.columns.values)

all_df_headers = np.append(df_headers_1_2, df_headers_3_4)

df_headers_to_translate = np.unique(all_df_headers)

translation = {'an':'age', 'mois':'month', 'jour':'day'}


print(all_df_headers)
print(df_headers_to_translate)
#print(type(all_df_headers))

# CS 6350.001 Big Data Management & Analytics Final Project
# Using ML techniques to predict information about phramacies

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

if __name__ == "__main__":
    df_pharmacies = pd.read_csv('./Data/Pharmacy-County.csv').dropna(thresh=3)
    df_demographics = pd.read_csv('./Data/Demography_USA.csv').dropna(thresh=3)

    # Collect Metadata
    list_states = df_pharmacies['State'].unique()
    list_cities = df_pharmacies.drop_duplicates(subset=['State', 'City'])

    # Print Metadata
    print("------------------------------------OVERVIEW------------------------------------")
    print(df_pharmacies[['City','State']].value_counts())
    print('{:<40}{:>40}'.format('\nAverage # of Pharmacies per City: ', df_pharmacies[['City','State']].value_counts().mean()))
    print('{:<40}{:>40}'.format('Total # of States/Territories:', len(list_states)))
    print('{:<20}{:>60}'.format('States/Territories:', ','.join(list_states)))
    print('{:<40}{:>40}'.format('Total # of Cities:', len(list_cities)))
    print('{:<40}{:>40}'.format('Total # of Pharmacies:', len(df_pharmacies)))
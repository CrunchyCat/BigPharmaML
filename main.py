# CS 6350.001 Big Data Management & Analytics Final Project
# Using ML techniques to predict information about phramacies

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import linear_model
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

if __name__ == "__main__":
    df_pharmacies = pd.read_csv('./Data/Pharmacy-County.csv').dropna(thresh=3)
    df_demographics = pd.read_csv('./Data/Demography_USA_Normalized.csv').dropna(thresh=3)

    # Collect Metadata
    list_states = df_pharmacies['State'].unique()
    list_cities = df_pharmacies.drop_duplicates(subset=['State', 'City'])

    # Print Metadata
    print("------------------------------------OVERVIEW------------------------------------")
    print(df_pharmacies[['City','State']].value_counts())
    print('{:<40}{:>40}'.format('\nAverage # of Pharmacies per State: ', df_pharmacies[['State']].value_counts().mean()))
    print('{:<40}{:>40}'.format('Average # of Pharmacies per City: ', df_pharmacies[['City','State']].value_counts().mean()))
    print('{:<40}{:>40}'.format('Total # of States/Territories:', len(list_states)))
    print('{:<20}{:>60}'.format('States/Territories:', ','.join(list_states)))
    print('{:<40}{:>40}'.format('Total # of Cities:', len(list_cities)))
    print('{:<40}{:>40}'.format('Total # of Pharmacies:', len(df_pharmacies)))

    # Initialize Data Scaler
    scaler = StandardScaler()

    # Predict Cardiovascular Disease (CVD)
    X = scaler.fit_transform(df_demographics[['POP13_SQMI','MED_AGE','MED_AGE_M','MED_AGE_F']])
    y = df_demographics['Diabetes']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 42)
    regr = linear_model.LinearRegression()

    # Fit the Model
    regr.fit(X_train, y_train)

    # Predit the Test Data
    score = regr.score(X_test, y_test)
    print('Score', score)
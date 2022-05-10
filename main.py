# CS 6350.001 Big Data Management & Analytics Final Project
# Using ML techniques to predict information about phramacies

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn import linear_model
# import matplotlib.pyplot as plt

NUM_ITERATIONS = 5 # Number of Times to Run the Model to Avg Accuracy

if __name__ == "__main__":
    df_pharmacies = pd.read_csv('./Data/Pharmacy-County.csv').dropna(thresh=3)
    df_demographics = pd.read_csv('./Data/Demography_USA_Normalized_Clean.csv').dropna(thresh=3)

    # Collect Metadata
    list_states = df_pharmacies['State'].unique()
    list_cities = df_pharmacies.drop_duplicates(subset=['State', 'City'])
    pharmas_per_state = df_pharmacies['State'].value_counts()
    pharmas_per_city = df_pharmacies[['City','State']].value_counts()

    # Print Metadata
    print("------------------------------------OVERVIEW------------------------------------")
    print(df_pharmacies[['City','State']].value_counts())
    print('{:<40}{:>40}'.format('\nAverage # of Pharmacies per State: ', pharmas_per_state.mean()))
    print('{:<40}{:>40}'.format('Average # of Pharmacies per City: ', pharmas_per_city.mean()))
    print('{:<40}{:>40}'.format('Total # of States/Territories:', len(list_states)))
    print('{:<20}{:>60}'.format('States/Territories:', ','.join(list_states)))
    print('{:<40}{:>40}'.format('Total # of Cities:', len(list_cities)))
    print('{:<40}{:>40}'.format('Total # of Pharmacies:', len(df_pharmacies)))

    print('{:<40}{:>40}'.format('\nAverage Population % with Diabetes: ', df_demographics['Diabetes'].min()))

    ########################################################################################################################
    # Normalized Features:
    # "Prevalence of obesity", "Diabetes", "HIV/AIDS", "WHITE", "BLACK", "AMERI_ES", "ASIAN", "HAWN_PI", "HISPANIC",
    # "OTHER", "MULT_RACE", "MALES", "FEMALES", "AGE_UNDER5", "AGE_5_9", "AGE_10_14", "AGE_15_19", "AGE_20_24",
    # "AGE_25_34", "AGE_35_44", "AGE_45_54", "AGE_55_64", "AGE_65_74", "AGE_75_84", "AGE_85_UP", "cvd_100k",
    # "hypertension_100k"

    # Independent Class Features:
    # "City", "State", "STATE_FIPS", "CNTY_FIPS", "FIPS", "IECC Climate Zone", "IECC Moisture Regime",
    # "BA Climate Zone", "County Name"

    # Independent Value Features:
    # "POP10_SQMI", "POP13_SQMI", "MED_AGE", "MED_AGE_M", "MED_AGE_F", "Temp"

    # Semi-Indepedent Value Features (Use with Caution):
    # "POP2010", "POP2013", "SQMI"
    ########################################################################################################################

    # Initialize Models
    regr = RandomForestRegressor()

    # Predict Cardiovascular Disease Diabetes from Age Demographics
    df_cut = df_demographics[['Diabetes', 'AGE_75_84', 'Prevalence of obesity', 'HIV/AIDS', 'WHITE', 'BLACK', 'AMERI_ES', 'ASIAN', 'HAWN_PI', 'HISPANIC', 'OTHER', 'MULT_RACE', 'cvd_100k', 'hypertension_100k', 'Temp']]
    df_demo_filt = df_cut[df_cut.all(1)] # Remove Negative Values
    X = df_demo_filt[['AGE_75_84', 'Prevalence of obesity', 'HIV/AIDS', 'WHITE', 'BLACK', 'AMERI_ES', 'ASIAN', 'HAWN_PI', 'HISPANIC', 'OTHER', 'MULT_RACE', 'cvd_100k', 'hypertension_100k', 'Temp']]
    y = df_demo_filt['Diabetes']

    sum_score = 0.0
    for i in range(NUM_ITERATIONS):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3)

        # Fit the Model
        regr.fit(X_train, y_train)

        # Predit the Test Data
        sum_score += regr.score(X_test, y_test)
    print('{:<40}{:>40}'.format('Predicting % Diabetes in Population:', sum_score / NUM_ITERATIONS))

    # Predict Cardiovascular Disease Diabetes from Age Demographics
    df_cut = df_demographics[['AGE_75_84', 'Prevalence of obesity', 'HIV/AIDS', 'WHITE', 'BLACK', 'AMERI_ES', 'ASIAN', 'HAWN_PI', 'HISPANIC', 'OTHER', 'MULT_RACE', 'cvd_100k', 'hypertension_100k', 'Temp']]
    df_demo_filt = df_cut[df_cut.all(1)] # Remove Negative Values
    X = df_demo_filt[['Prevalence of obesity', 'HIV/AIDS', 'WHITE', 'BLACK', 'AMERI_ES', 'ASIAN', 'HAWN_PI', 'HISPANIC', 'OTHER', 'MULT_RACE', 'cvd_100k', 'hypertension_100k', 'Temp']]
    y = df_demo_filt['AGE_75_84']

    sum_score = 0.0
    for i in range(NUM_ITERATIONS):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3)

        # Fit the Model
        regr.fit(X_train, y_train)

        # Predit the Test Data
        sum_score += regr.score(X_test, y_test)
    print('{:<40}{:>40}'.format('Predicting Population 85+ %:', sum_score / NUM_ITERATIONS))
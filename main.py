# CS 6350.001 Big Data Management & Analytics Final Project
# Using ML techniques to predict information about phramacies

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

if __name__ == "__main__":
    df_pharmacies = pd.read_csv('./Data/Pharmacy-County.csv').dropna(thresh=3)
    df_demographics = pd.read_csv('./Data/Demography_USA.csv').dropna(thresh=3)
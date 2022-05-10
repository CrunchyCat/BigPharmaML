# CS 6350.001 Big Data Management & Analytics Final Project
# Using ML techniques to predict information about phramacies

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import linear_model
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score
import seaborn as sns

if __name__ == "__main__":
    df_pharmacies = pd.read_csv('./Data/Pharmacy-County.csv').dropna(thresh=3)
    df_demographics = pd.read_csv('./Data/Demography_USA_Normalized_Clean.csv').dropna(thresh=3)

    #corelation between every features
    cmatrix = df_demographics.corr()
    print(pd.DataFrame(cmatrix))
    sns.heatmap(cmatrix, annot= True)
    plt.show()
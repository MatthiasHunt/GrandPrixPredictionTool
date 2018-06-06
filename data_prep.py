import pandas as pd
from sklearn import preprocessing
import numpy as np


def get_data():
    """Reads from enhanced_data.csv and returns a tuple of (X values, attendance, future events)"""
    # Importing and transforming our Dataset
    gp_data = pd.read_csv("enhanced_data.csv",index_col = 0)
    gp_data = gp_data.drop('Location',axis=1)
    
    # Through Backwards Elimnation code in Linear Regression, Month was found to be non-predictive
    gp_data = gp_data.drop('Month',axis = 1)
    X = gp_data.iloc[:, :-1].values
    y = gp_data.iloc[:,4].values
    
    # Labeling Categorical Data
    label_encoder = preprocessing.LabelEncoder()
    categorical_columns = [1,2]
    for col in categorical_columns:
        X[:,col] = label_encoder.fit_transform(X[:,col])
    X = X[:,:].astype(int)
    
    # Dummy encoding
    count = 0
    for a,b in enumerate(categorical_columns):
        hot_encoder = preprocessing.OneHotEncoder(categorical_features = [count + b - 2*a])
        hot_encoder.fit(X)
        count = count + (hot_encoder.n_values_)
        X = hot_encoder.fit_transform(X).toarray()
        X = X[:,1:]
        
    #Separating out Past events from future ones
    future_events = gp_data.loc[gp_data['Attendance'].isnull()].index.values
    past_events = gp_data.loc[gp_data['Attendance'].notnull()].index.values
    X_future = X[future_events,:]
    X = X[past_events,:]
    y = y[~np.isnan(y)]
    
    return (X,y,X_future,gp_data)
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.tree import export_graphviz
import pydot
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

def main():
    
    gp_data = pd.read_csv("enhanced_data.csv",index_col = 0)
    gp_data = gp_data.drop('Location',axis=1)
    gp_data = gp_data.dropna()
    gp_data = pd.get_dummies(gp_data)

    y_col = gp_data.pop('Attendance')
    col_names = gp_data.columns
    gp_data['Attendance'] = y_col
    X = gp_data.iloc[:, :-1].values
    y = gp_data.iloc[:,36].values

    X_train, X_test, y_train, y_test = train_test_split(X[:,:], y, test_size = 0.2)

    regressor = RandomForestRegressor(n_estimators= 1000)
    regressor.fit(X_train,y_train)

    # Use line to create a tree visualization
    create_tree_png(regressor,col_names,6)
    
    # Analyze Feature Importance
    print_feature_importance(regressor,col_names)
    
    # Prediction values
    y_pred = regressor.predict(X_test).astype(int)
    y_delta = abs(y_pred-y_test)
      
    
    ### STILL TO DO
    
    # Predict Future attendances

    # Visualize Results

def create_tree_png(rf,col_names,tree_index):
    tree = rf.estimators_[tree_index]
    export_graphviz(tree, out_file = 'tree.dot', feature_names = col_names, rounded = True, precision = 1)
    (graph, ) = pydot.graph_from_dot_file('tree.dot')
    graph.write_png('tree.png')
    
def print_feature_importance(rf,col_names):
    importances = list(rf.feature_importances_)
    feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(col_names, importances)]
    feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)
    [print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importances];
    
if __name__ == '__main__':
    main()
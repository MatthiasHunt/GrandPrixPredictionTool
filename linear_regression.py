import numpy as np
import matplotlib.pyplot as plt
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LinearRegression
import statsmodels.formula.api as sm
import data_prep


def main():
    
    (X,y,X_future,gp_data) = data_prep.get_data()
        
    # Splitting the data into Training and Test Sets
    X_train, X_test, y_train, y_test = train_test_split(X[:,:], y, test_size = 0.2)
    
    # Fitting Multiple Linear Regression to the Training set
    regressor = LinearRegression()
    regressor.fit(X_train, y_train)
    
    # Prediction values
    y_pred = regressor.predict(X_test).astype(int)
    y_delta = y_pred-y_test
      
    # Visualizing Our Model's accuracy
    plt.figure(1)
    plt.scatter(y_test,y_delta, color = 'red')
    plt.title('Baseline Accuracy (Linear Regression)')
    plt.xlabel('Actual Event Attendance')
    plt.ylabel('Error in Linear Prediction')
    
    # Determining Which Variables Carry Significance
    format_weights = {'Block Constructed':0.}
    for i in range(12):
        try:
            format_weights[gp_data['Format'][np.where(X[:,i]==1)[0][0]]] = regressor.coef_[i]
        except:
            continue
    
    # Re-Center data on Standard For readability and sort
    for gp_format in format_weights:
        format_weights[gp_format] -= format_weights['Standard']
    format_weights.pop('Standard')
    sorted_X = sorted(list(format_weights.values()))
    sorted_y = []
    for i in range(len(sorted_X)):
        sorted_y.append([key for key,value in format_weights.items() if value == sorted_X[i]][0])
    
    # Create Bar Graphs
    plt.figure(2)
    index = np.arange(len(format_weights))
    plt.barh(index,list(sorted_X))
    plt.ylabel('New Grand Prix Format')
    plt.xlabel('Expected Change in Attendance')
    plt.title('Format Attendance Compared to Standard (Linear Approximation)')
    plt.yticks(index,sorted_y,fontsize = 8, rotation = 30)
    
    plt.show()

def backwards_elim(X,y):
    #Backwards Elimination model Loop as needed. Not used in final implementations
    X = np.append(arr = np.ones((618,1)).astype(int), values = X, axis=1)
    X_optimal = X[:,:]
    regressor_least_squares = sm.OLS(endog = y, exog = X_optimal).fit()
    regressor_least_squares.summary()
    
if __name__ == '__main__':
    main()    
    
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import warnings



def marks_prediction(marks):
    data = pd.read_csv("student_scores.csv")
    x = data.iloc[:, :-1].values
    y = data.iloc[:, 1].values
    reg = LinearRegression()
    reg.fit(x, y)

    x_test=np.array(float(marks))
    x_test = x_test.reshape((1,-1))
    return reg.predict(x_test)



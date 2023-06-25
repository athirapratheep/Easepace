import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import warnings



def marks_prediction(marks,goals):
    data = pd.read_csv("student_scores.csv")
    x = data.iloc[:, :-1].values
    y = data.iloc[:, 1].values
    reg = LinearRegression()
    reg.fit(x, y)

    x_new = data.iloc[:, 1].values  # Marks
    y_new = data.iloc[:, 0].values  # Study Hours
    reg_new = LinearRegression()
    reg_new.fit(x_new.reshape(-1,1), y_new)

    x_test=np.array(float(marks))
    x_test = x_test.reshape((1,-1))
    new_test=np.array(float(goals))
    new_test=new_test.reshape((-1,1))
    return reg.predict(x_test),reg_new.predict(new_test)



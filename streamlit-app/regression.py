import streamlit as st
import numpy as np
import pandas as pd
from statsmodels.regression.linear_model import RegressionResults
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
import statsmodels.api as sm

# %%


def _get_model(df, regressand, regressors):

    x = sm.add_constant(df[regressors])
    y = df[regressand]

    model = sm.OLS(y, x)
    results = model.fit()

    return results


def view(**kwargs):

    st.write("## Multivariate Regression Model")

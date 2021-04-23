from django.shortcuts import render
from requests import Response
from tensorflow import keras
import numpy as np
from sklearn.preprocessing import StandardScaler
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from django.http import HttpResponse
from django.http import JsonResponse
import json


file = open("silver/ML_model/variables/dataset_train", "rb")
dataset_train = np.load(file)

file = open("silver/ML_model/variables/X_train", "rb")
X_train = np.load(file)

file = open("silver/ML_model/variables/n_past", "rb")
n_past = np.load(file)

file = open("silver/ML_model/variables/training_set", "rb")
training_set = np.load(file)

dataset = pd.read_csv('silver/ML_model/dataset.csv')

# Volatility
volatile = dataset[['Date', 'Adj Close']]
volatile = volatile.set_index('Date')
daily_simple_returns = volatile[['Adj Close']].pct_change(1)
daily_simple_returns = daily_simple_returns.dropna()


def analysis( request ):

    # Last Price
    last_price = dataset['Close'].tail(1)
    price = "{0:.2f}".format(float(last_price.values))

    # Volatility
    daily_simple_returns = volatile[['Adj Close']].pct_change(1)
    daily_simple_returns = daily_simple_returns.dropna()
    commo_volatility = "{0:.5f}".format(float(daily_simple_returns.std()))

    # Daily returns
    daily_mean_simple_returns = "{0:.5f}".format(float(daily_simple_returns.mean()))

    # Yearly returns
    yearly_mean_simple_returns = float(daily_mean_simple_returns) * 253

    context = {
        'last_price': price,
        'commo_volatility': commo_volatility,
        'daily_returns': daily_mean_simple_returns,
        'yearly_returns': yearly_mean_simple_returns,
    }
    return render(request, "silver/analysis.html", context=context)


def analysis_api( request ):

    # Close prices - Line chart
    close_prices = dataset[['Date', 'Close']]
    close_prices_labels = close_prices['Date'].tolist()
    close_prices_chartLabels = "Silver"
    close_prices_chartData = close_prices['Close'].tolist()

    # Volume - Bar chart
    volume = dataset[['Date', 'Volume']]
    volume_labels = volume['Date'].tolist()
    volume_chartLabels = "Silver"
    volume_chartData = volume['Volume'].tolist()

    # Volatility
    volatile_labels = daily_simple_returns.index.tolist()
    volatile_chartLabels = "Volatility"
    volatile_chartData = daily_simple_returns['Adj Close'].tolist()

    # Cumulative Returns
    dailyCumulSimpleReturn = (daily_simple_returns + 1).cumprod()
    cumulative_labels = dailyCumulSimpleReturn.index.tolist()
    cumulative_chartLabels = "Cumulative Returns"
    cumulative_chartData = dailyCumulSimpleReturn['Adj Close'].tolist()

    # Response
    data = {
        "close_data": {
            "labels": close_prices_labels,
            "chartLabel": close_prices_chartLabels,
            "chartdata": close_prices_chartData,
        },
        "volume_data": {
            "labels": volume_labels,
            "chartLabel": volume_chartLabels,
            "chartdata": volume_chartData,
        },
        "volatile_data": {
            "labels": volatile_labels,
            "chartLabel": volatile_chartLabels,
            "chartdata": volatile_chartData,
        },
        "cumulative_data": {
            "labels": cumulative_labels,
            "chartLabel": cumulative_chartLabels,
            "chartdata": cumulative_chartData,
        },
    }

    return JsonResponse(data, safe=False)


def forecast( request ):
    return render(request, "silver/forecast.html")

def forecast_api( request ):
    file = open("silver/ML_model/variables/n_future", "rb")
    n_future = np.load(file)
    n_future = int(n_future)

    model_new = keras.models.load_model('silver/ML_model/mymodel')

    # Perform predictions
    predictions_future = model_new.predict(X_train[-n_future:])
    predictions_train = model_new.predict(X_train[n_past:])

    sc = StandardScaler()
    training_set_scaled = sc.fit_transform(training_set)

    sc_predict = StandardScaler()
    sc_predict.fit_transform(training_set[:, 0:1])

    # Transform the predictions
    y_pred_future = sc_predict.inverse_transform(predictions_future)
    y_pred_train = sc_predict.inverse_transform(predictions_train)

    # Get the Date column
    dataset = pd.read_csv('silver/ML_model/dataset.csv')
    cols = list(dataset)[1:6]
    datelist_train = list(dataset['Date'])
    dataset = dataset[cols].astype(str)
    for i in cols:
        for j in range(0, len(dataset)):
            dataset[i][j] = dataset[i][j].replace(',', '')

    dataset = dataset.astype(float)

    datelist_future = pd.date_range(datelist_train[-1], periods=n_future, freq='1d').tolist()

    # Convert Pandas Timestamp to Datetime object (for transformation) --> FUTURE
    datelist_future_ = []
    for this_timestamp in datelist_future:
        datelist_future_.append(this_timestamp.date())

    PREDICTIONS_FUTURE = pd.DataFrame(y_pred_future, columns=['Open']).set_index(pd.Series(datelist_future))

    PREDICTIONS_FUTURE.reset_index(inplace=True)
    PREDICTIONS_FUTURE.rename(columns={'index': 'Date'}, inplace=True)

    # Response
    chart_labels = PREDICTIONS_FUTURE['Date'].tolist()
    chart_data = PREDICTIONS_FUTURE['Open'].tolist()
    data = {
        'labels': chart_labels,
        'data': chart_data,
    }
    return JsonResponse(data, safe=False)

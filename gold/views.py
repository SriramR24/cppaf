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

file = open("gold/ML_model/variables/dataset_train", "rb")
dataset_train = np.load(file)

file = open("gold/ML_model/variables/X_train", "rb")
X_train = np.load(file)

file = open("gold/ML_model/variables/n_past", "rb")
n_past = np.load(file)

file = open("gold/ML_model/variables/training_set", "rb")
training_set = np.load(file)

dataset = pd.read_csv('gold/ML_model/dataset.csv')

# Volatile
volatile = dataset[['Date', 'Adj Close']]
volatile = volatile.set_index('Date')
daily_simple_returns = volatile[['Adj Close']].pct_change(1)
daily_simple_returns = daily_simple_returns.dropna()


def analysis(request):

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
    return render(request, "gold/analysis.html", context=context)


def analysis_api(request):

    # Close price - Line chart
    close_prices = dataset[['Date', 'Close']]
    close_prices_labels = close_prices['Date'].tolist()
    close_prices_chartLabels = "Gold"
    close_prices_chartData = close_prices['Close'].tolist()

    # Volume - Bar chart
    volume = dataset[['Date', 'Volume']]
    volume_labels = volume['Date'].tolist()
    volume_chartLabels = "Volume"
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
    return render(request, "gold/forecast.html")


def forecast_api( request ):

    dataset = pd.read_csv('gold/ML_model/dataset.csv')
    print(dataset)


            # RSI

    # Get the difference in price from the previous day
    delta = dataset['Adj Close'].diff(1)
    print(f"Delta = {delta}")
    # Get rid of NaN
    delta = delta.dropna()
    print(f"Delta = {delta}")

    # Get the positive gains (up) and the negative gains (down)
    up = delta.copy()
    down = delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0

    # Get the time period
    period = 14  # RSI uses 14 day time period

    # Calculate the avg gain and avg loss
    AVG_Gain = up.rolling(window=period).mean()
    AVG_Loss = abs(down.rolling(window=period).mean())

    # Calculate the RSI
    # Calculate the Relative Strength (RS)
    RS = AVG_Gain / AVG_Loss
    # Calculate the RSI
    RSI = 100.0 - (100.0 / (1.0 + RS))
    print(f"RSI = {RSI}")

    # Create a new DF
    new_df = pd.DataFrame()
    new_df['Date'] = dataset['Date']
    new_df['Adj Close'] = dataset['Adj Close']
    new_df['RSI'] = RSI
    new_df = new_df.set_index(pd.DatetimeIndex(new_df['Date'].values))
    mean_value = new_df['RSI'].mean()
    print(f"Mean = {mean_value}")
    new_df['RSI'].fillna(value=mean_value, inplace=True)
    print(f"New_df = {new_df}")

    rsi_chartLabels = new_df['Date'].tolist()
    rsi_chartData = new_df['RSI'].tolist()

            # END OF RSI


            # PREDICTION

    file = open("gold/ML_model/variables/n_future", "rb")
    n_future = np.load(file)
    n_future = int(n_future)

    model_new = keras.models.load_model('gold/ML_model/mymodel')

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
    dataset = pd.read_csv('gold/ML_model/dataset.csv')
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
    # PREDICTIONS_FUTURE.Date = pd.to_datetime(PREDICTIONS_FUTURE.Date, format='%Y-%m-%d')

            # END OF PREDICTION

            # Response

    predict_chartLabels = PREDICTIONS_FUTURE['Date'].tolist()
    predict_chartData = PREDICTIONS_FUTURE['Open'].tolist()

    data = {
        'rsi_data': {
            'labels': rsi_chartLabels,
            'data': rsi_chartData,
        },
        'predict_data': {
            'labels': predict_chartLabels,
            'data': predict_chartData,
        },
    }
    return JsonResponse(data, safe=False)

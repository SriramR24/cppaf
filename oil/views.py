import numpy as np
import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse


dataset = pd.read_csv('oil/ML_model/dataset.csv')

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
    return render(request, "oil/analysis.html", context=context)


def analysis_api( request ):

    # Close price - Line chart
    close_prices = dataset[['Date', 'Close']]
    close_prices_labels = close_prices['Date'].tolist()
    close_prices_chartLabels = "Close price"
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

    # Last Price
    last_price = dataset['Close'].tail(1)
    price = "{0:.2f}".format(float(last_price.values))

    file = open("oil/ML_model/variables/PREDICTIONS_FUTURE", "rb")
    PREDICTIONS_FUTURE = np.load(file)
    print(PREDICTIONS_FUTURE, len(PREDICTIONS_FUTURE))

    # Price after 30/60 days
    price_after_30_days = "{0:.2f}".format(float(PREDICTIONS_FUTURE[29]))
    price_after_60_days = "{0:.2f}".format(float(PREDICTIONS_FUTURE[59]))

    # %change
    x = np.reshape(PREDICTIONS_FUTURE, (60))
    list_series = pd.Series(x).pct_change(1)
    per_change = "{0:.5f}".format(list_series.loc[59])

    context = {
        'last_price': price,
        'price_after_30_days': price_after_30_days,
        'price_after_60_days': price_after_60_days,
        'per_change': per_change,
    }

    return render(request, "oil/forecast.html", context=context)


def forecast_api( request ):

    # RSI
    new_df = get_rsi_data()

    rsi_chartLabels = new_df['Date'].tolist()
    rsi_chartData = new_df['RSI'].tolist()

    # MACD
    MACD_df = get_macd_data()

    macd_chartLabels = MACD_df['Date'].tolist()
    macd_chartData = MACD_df['MACD'].tolist()
    signal_chartData = MACD_df['Signal'].tolist()

    # BUY/SELL SIGNALS
    buysell_df = get_buysell_data(MACD_df)

    buysell_chartLabels = buysell_df['Date'].tolist()
    close_chartData = buysell_df['Close'].tolist()
    buy_chartData = buysell_df['Buy_signals'].fillna("null").tolist()
    sell_chartData = buysell_df['Sell_signals'].fillna("null").tolist()

    # Response
    data = {
        # "predict_data": {
        #     'labels': chart_labels,
        #     'data': chart_data,
        # }
        'rsi_data': {
            'labels': rsi_chartLabels,
            'data': rsi_chartData,
        },
        'macd_data': {
            'labels': macd_chartLabels,
            'data': {
                'macd': macd_chartData,
                'signal': signal_chartData,
            },
        },
        'buysell_data': {
            'labels': buysell_chartLabels,
            'data': {
                'close': close_chartData,
                'buy': buy_chartData,
                'sell': sell_chartData,
            },
        },
    }
    return JsonResponse(data, safe=False)


def get_rsi_data():

    # Get the difference in price from the previous day
    delta = dataset['Adj Close'].diff(1)
    # Get rid of NaN
    delta = delta.dropna()

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

    # Create a new DF
    new_df = pd.DataFrame()
    new_df['Date'] = dataset['Date']
    new_df['Adj Close'] = dataset['Adj Close']
    new_df['RSI'] = RSI
    new_df = new_df.set_index(pd.DatetimeIndex(new_df['Date'].values))
    mean_value = new_df['RSI'].mean()
    new_df['RSI'].fillna(value=mean_value, inplace=True)

    return new_df

def get_macd_data():

    # Calc the short term expon. mov. avg. (EMA)
    ShortEMA = dataset.Close.ewm(span=12, adjust=False).mean()
    # Calc the long term expon. mov. avg. (EMA)
    LongEMA = dataset.Close.ewm(span=26, adjust=False).mean()
    # Calc the MACD line
    MACD = ShortEMA - LongEMA
    # Calc the signal line
    signal = MACD.ewm(span=9, adjust=False).mean()
    MACD_df = pd.DataFrame()
    MACD_df['Date'] = dataset['Date']
    MACD_df['MACD'] = MACD
    MACD_df['Signal'] = signal

    return MACD_df


def get_buysell_data(df):

    df['Close'] = dataset['Close']

    def buy_sell(signal):
        buy = []
        sell = []
        flag = -1

        for i in range(0, len(signal)):
            if signal['MACD'][i] > signal['Signal'][i]:
                sell.append(np.nan)
                if flag != 1:
                    buy.append(signal['Close'][i])
                    flag = 1
                else:
                    buy.append(np.nan)
            elif signal['MACD'][i] < signal['Signal'][i]:
                buy.append(np.nan)
                if flag != 0:
                    sell.append(signal['Close'][i])
                    flag = 0
                else:
                    sell.append(np.nan)
            else:
                buy.append(np.nan)
                sell.append(np.nan)

        return (buy, sell)

    # Create a buy and sell column
    a = buy_sell(df)
    df['Buy_signals'] = a[0]
    df['Sell_signals'] = a[1]

    return df


# def get_predictions_data():
#     file = open("silver/ML_model/variables/n_future", "rb")
#     n_future = np.load(file)
#     n_future = int(n_future)
#
#     model_new = keras.models.load_model('silver/ML_model/mymodel')
#
#     # Perform predictions
#     predictions_future = model_new.predict(X_train[-n_future:])
#     predictions_train = model_new.predict(X_train[n_past:])
#
#     sc = StandardScaler()
#     training_set_scaled = sc.fit_transform(training_set)
#
#     sc_predict = StandardScaler()
#     sc_predict.fit_transform(training_set[:, 0:1])
#
#     # Transform the predictions
#     y_pred_future = sc_predict.inverse_transform(predictions_future)
#     y_pred_train = sc_predict.inverse_transform(predictions_train)
#
#     # Get the Date column
#     dataset = pd.read_csv('silver/ML_model/dataset.csv')
#     cols = list(dataset)[1:6]
#     datelist_train = list(dataset['Date'])
#     dataset = dataset[cols].astype(str)
#     for i in cols:
#         for j in range(0, len(dataset)):
#             dataset[i][j] = dataset[i][j].replace(',', '')
#
#     dataset = dataset.astype(float)
#
#     datelist_future = pd.date_range(datelist_train[-1], periods=n_future, freq='1d').tolist()
#
#     # Convert Pandas Timestamp to Datetime object (for transformation) --> FUTURE
#     datelist_future_ = []
#     for this_timestamp in datelist_future:
#         datelist_future_.append(this_timestamp.date())
#
#     PREDICTIONS_FUTURE = pd.DataFrame(y_pred_future, columns=['Open']).set_index(pd.Series(datelist_future))
#
#     PREDICTIONS_FUTURE.reset_index(inplace=True)
#     PREDICTIONS_FUTURE.rename(columns={'index': 'Date'}, inplace=True)
#
#     return PREDICTIONS_FUTURE
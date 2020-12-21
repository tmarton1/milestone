# importing libraries
from flask import Flask, render_template, request, redirect
import requests
import pandas as pd
from bokeh.plotting import figure
from bokeh.embed import components
import datetime

def get_date_string(first_date,delta_days):
    date_format='%Y-%m-%d'
    date=first_date+datetime.timedelta(days=delta_days)
    if int(date.strftime('%w')) in range(1,6):
        return date.strftime(date_format)
    else:
        pass
    
# function to get data
def getData(ticker):
    reqUrl = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol='+ticker+'&apikey=ML4QI9IK9E7OVNPV'
    r=requests.get(reqUrl)
    return_data=r.json()

    date_format='%Y-%m-%d'
    last_date=datetime.datetime.strptime('2020-10-31',date_format)
    first_date=datetime.datetime.strptime('2020-09-30',date_format)
    max_delta_days=(last_date-first_date).total_seconds()/(24*60*60)

    date_strings=[(delta_days,get_date_string(first_date,delta_days)) for delta_days in range(1,int(max_delta_days)+1)]

    prices=[]
    dates=[]
    days=[]
    for ds in date_strings:
        try:
            price=float(return_data['Time Series (Daily)'][ds[1]]['4. close'])
            prices.append(price)
            dates.append(ds[1])
            days.append(ds[0])
        except:
            pass
    df=pd.DataFrame(list(zip(dates,days,prices)), columns=['date','day','closing price'])
    return df


# function to get plot
def getPlot(df, ticker):
    p = figure(title="Alphavantage Closing Stock prices 2020, Month of October", x_axis_label="Day in October",
               y_axis_label="Stock price", x_axis_type='datetime', plot_width=400)

    p.annulus(x=df['day'], y=df['closing price'], color='red', legend_label=ticker,inner_radius=0.2, outer_radius=0.25)
    p.line(x=df['day'], y=df['closing price'], color='red')
    return p


app = Flask(__name__)


@app.route('/')
def main():
    return redirect('/index')


@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/about', methods=['GET', 'POST'])
def about():
    # User inputs from the index.html
    ticker = request.form['ticker']
    ticker = ticker.upper()

    data = getData(ticker)
    plot = getPlot(data, ticker)

    script, div = components(plot)
    return render_template('about.html', script=script, div=div, reqUrl=reqUrl)


if __name__ == '__main__':
    #  app.run(host='0.0.0.0', port=33507)
    app.run(port=33507)

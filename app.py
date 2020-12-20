# importing libraries
from flask import Flask, render_template, request, redirect
import requests
import pandas as pd
from bokeh.plotting import figure
from bokeh.embed import components


# function to get data
def getData(ticker):
    # requesting data from Quandl
    start = "2020-11-01"
    end = "2020-11-30"
    reqUrl = 'https://www.quandl.com/api/v3/datasets/WIKI/' + ticker + '.json?start_date=' + start \
              + '&end_date=' + end + '&api_key=ky4zqe5WFwms5Tx2NXGx'
    r = requests.get(reqUrl)

    # fetch data
    return_data = r.json()['dataset']
    df = pd.DataFrame(return_data['data'], columns=return_data['column_names'])
    df.columns = [col.lower() for col in df.columns]
    df = df.set_index(pd.DatetimeIndex(df['date']))
    return df


# function to get plot
def getPlot(df, priceTypes, ticker):
    p = figure(title="Quandl End of Day Stock prices 2020, Month of November", x_axis_type="datetime", x_axis_label="Date",
               y_axis_label="Stock price", plot_width=1000)

    mapping = {'open': 'open', 'adjOpen': 'adj. open', 'close': 'close', 'adjClose': 'adj. close'}
    colour = {'open': 'orange', 'adjOpen': 'red', 'close': 'blue', 'adjClose': 'green'}

    for priceType in priceTypes:
        p.line(df.index, df[mapping[priceType]], color=colour[priceType], legend=ticker + ": " + mapping[priceType])
    return p


app = Flask(__name__)


@app.route('/')
def main():
    return redirect('/index')


@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/graph', methods=['GET', 'POST'])
def graph():
    # User inputs from the index.html
    ticker = request.form['ticker']
    ticker = ticker.upper()
    priceTypes = request.form.getlist('priceType')

    data = getData(ticker)
    plot = getPlot(data, priceTypes, ticker)

    script, div = components(plot)
    reqUrl = "https://www.google.com/finance?q=" + ticker
    return render_template('graph.html', script=script, div=div, reqUrl=reqUrl)


if __name__ == '__main__':
    #  app.run(host='0.0.0.0', port=33507)
    app.run(port=33507)

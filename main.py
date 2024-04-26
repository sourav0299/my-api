from flask import Flask, jsonify
import yfinance as yf
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# List of ticker symbols for the portfolio
portfolio_symbols = ['AAPL','GAIL.NS', 'IDFCFIRSTB.NS', 'IOC.NS', 'IRFC.NS', 'JIOFIN.NS', 'NBCC.NS', 'NCC.NS', 'ONGC.NS', 'SAIL.NS', 'TATAPOWER.NS', 'TATASTEEL.NS', 'TNPETRO.NS', 'ZOMATO.NS']

@app.route('/api/ltp/portfolio', methods=['GET'])
def get_portfolio_ltp():
    try:
        portfolio_ltp = {}
        for symbol in portfolio_symbols:
            # Fetch the data
            data = yf.Ticker(symbol)

            # Get the last price
            last_price = data.history(period="1d")["Close"].iloc[-1]

            # Add the symbol and last price to the portfolio dictionary
            portfolio_ltp[symbol] = last_price

        return jsonify(portfolio_ltp)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

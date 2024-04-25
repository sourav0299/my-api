from flask import Flask, jsonify, request
import yfinance as yf
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# List of ticker symbols for the portfolio
portfolio_symbols = ['GAIL.NS', 'IDFCFIRSTB.NS', 'IOC.NS', 'IRFC.NS', 'JIOFIN.NS', 'NBCC.NS', 'NCC.NS', 'ONGC.NS', 'SAIL.NS', 'TATAPOWER.NS', 'TATASTEEL.NS', 'TNPETRO.NS', 'ZOMATO.NS']

@app.route('/api/ltp/portfolio', methods=['GET'])
def get_portfolio_ltp():
    try:
        portfolio_ltp = {}
        for symbol in portfolio_symbols:
            # Fetch the data
            data = yf.Ticker(symbol)

            # Get the last price
            last_price = data.history(period="1d")["Close"].iloc[-1]

            # Round the last price to two decimal places
            last_price = round(last_price, 2)

            # Add the symbol and last price to the portfolio dictionary
            portfolio_ltp[symbol] = last_price

        return jsonify(portfolio_ltp), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

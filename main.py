from flask import Flask, jsonify
from flask_socketio import SocketIO
import yfinance as yf
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app)

# List of ticker symbols for the portfolio
portfolio_symbols = ['GAIL.NS', 'IDFCFIRSTB.NS', 'IOC.NS', 'IRFC.NS', 'JIOFIN.NS', 'NBCC.NS', 'NCC.NS', 'ONGC.NS', 'SAIL.NS', 'TATAPOWER.NS', 'TATASTEEL.NS', 'TNPETRO.NS', 'ZOMATO.NS']

def update_prices():
    while True:
        try:
            portfolio_ltp = {}
            for symbol in portfolio_symbols:
                # Fetch the data
                data = yf.Ticker(symbol)

                # Get the last price
                last_price = data.history(period="1d")["Close"].iloc[-1]

                # Add the symbol and last price to the portfolio dictionary
                portfolio_ltp[symbol] = last_price

            # Emit updated prices to connected clients
            socketio.emit('portfolio_prices', portfolio_ltp)

            # Sleep for a short interval before updating again
            time.sleep(5)  # Update every 5 seconds, adjust as needed
        except Exception as e:
            print("Error:", e)
            # If an error occurs, continue updating after a short delay
            time.sleep(10)  # Wait for 10 seconds before retrying

@app.route('/')
def index():
    return "Real-time Portfolio Prices API"

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    # Start the price update thread
    update_thread = threading.Thread(target=update_prices)
    update_thread.daemon = True
    update_thread.start()

    # Start the Flask-SocketIO server
    socketio.run(app, host='0.0.0.0', port=8080)

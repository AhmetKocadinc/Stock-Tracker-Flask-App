from flask import Flask, render_template, request, jsonify
import yfinance as yf
import matplotlib

matplotlib.use('Agg')  # GUI modunu devre dışı bırakıyoruz, grafik kaydedilecek.
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# En popüler 10 hisse senedi sembolleri
popular_stocks = ['AAPL', 'TSLA', 'MSFT', 'AMZN', 'GOOGL', 'META', 'NFLX', 'NVDA', 'BABA', 'DIS']


@app.route('/')
def index():
    return render_template('index.html', stocks=popular_stocks)


@app.route('/get_stock_data', methods=['POST'])
def get_stock_data():
    stock_symbol = request.json['stock_symbol']  # Seçilen hisse senedi sembolü alınıyor
    stock = yf.Ticker(stock_symbol)

    # Hisse senedi verilerini çekme
    stock_data = stock.history(period='1mo')

    # Grafik oluşturma
    plt.figure(figsize=(10, 5))
    plt.plot(stock_data.index, stock_data['Close'], label='Close Price', color='blue')
    plt.title(f'{stock_symbol} Close Price - Last 1 Month')
    plt.xlabel('Date')
    plt.ylabel('Price ($)')
    plt.grid(True)
    plt.legend()

    # Grafiği statik klasöre kaydetme
    img_path = f'static/{stock_symbol}_plot.png'
    plt.savefig(img_path)
    plt.close()

    # Grafiğin yolunu JSON olarak geri döndürme
    return jsonify({'img_path': img_path})


if __name__ == '__main__':
    app.run(debug=True)

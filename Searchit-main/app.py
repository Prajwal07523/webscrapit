from flask import Flask, render_template, request, redirect, url_for
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

def extract_ethereum_wallet_addresses(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            page_text = soup.get_text()
            ethereum_pattern = r'0x[a-fA-F0-9]{40}'
            ethereum_addresses = re.findall(ethereum_pattern, page_text)
            unique_addresses = list(set(ethereum_addresses))
            return unique_addresses
        else:
            return []
    except Exception as e:
        return []

@app.route('/', methods=['GET', 'POST'])
def index():
    wallet_addresses = []
    if request.method == 'POST':
        url = request.form['url']
        wallet_addresses = extract_ethereum_wallet_addresses(url)
    return render_template('index.html', wallet_addresses=wallet_addresses)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000)
    

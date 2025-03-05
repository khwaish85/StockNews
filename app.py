from flask import Flask, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import moneycontrol.moneycontrol_api as mc_api

app = Flask(__name__)
CORS(app)  # Enable CORS

MONEYCONTROL_URL = "https://www.moneycontrol.com/news/"  # Replace with the actual API if available

@app.route("/")
def home():
    return jsonify({"message": "Hello from Flask API!"})

@app.route("/news", methods=["GET"])
def get_news():
    try:
        news = mc_api.get_news()  # Fetches news from Moneycontrol API
        return jsonify(news)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_moneycontrol_news', methods=['GET'])
def get_moneycontrol_news():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(MONEYCONTROL_URL, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = []

        # Extract top headlines from Moneycontrol (Modify based on Moneycontrol's HTML structure)
        news_items = soup.select('.clearfix')[:10]  # Modify selector as per Moneycontrol's structure

        for item in news_items:
            title = item.find('h2')  # Example: Adjust according to Moneycontrol's structure
            link = item.find('a', href=True)
            if title and link:
                articles.append({
                    "title": title.text.strip(),
                    "link": link['href']
                })

        return jsonify(articles)

    return jsonify({"error": "Failed to fetch data"}), 500

if __name__ == "__main__":
    app.run(host="192.168.25.22", port=5001, debug=True)
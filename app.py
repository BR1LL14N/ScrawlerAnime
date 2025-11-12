from flask import Flask, render_template, jsonify
import json
import os
from scraper import AnimeScraper

app = Flask(__name__)
scraper = AnimeScraper()

def load_json(filename):
    """Load JSON file"""
    try:
        with open(f'results/{filename}', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/scrape-all')
def scrape_all():
    """Scrape both websites in parallel"""
    try:
        result = scraper.scrape_parallel()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/scrape-otakudesu')
def scrape_otakudesu():
    """Scrape OtakuDesu only"""
    try:
        result = scraper.scrape_otakudesu()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/scrape-kusonime')
def scrape_kusonime():
    """Scrape Kusonime only"""
    try:
        result = scraper.scrape_kusonime()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/otakudesu')
def view_otakudesu():
    """View OtakuDesu results"""
    data = load_json('otakudesu.json')
    return render_template('otakudesu.html', data=data)

@app.route('/kusonime')
def view_kusonime():
    """View Kusonime results"""
    data = load_json('kusonime.json')
    return render_template('kusonime.html', data=data)

@app.route('/comparison')
def comparison():
    """View comparison of both sites"""
    otakudesu = load_json('otakudesu.json')
    kusonime = load_json('kusonime.json')
    return render_template('comparison.html', otakudesu=otakudesu, kusonime=kusonime)

@app.route('/api/otakudesu')
def api_otakudesu():
    """API endpoint for OtakuDesu JSON"""
    data = load_json('otakudesu.json')
    if data:
        return jsonify(data)
    return jsonify({'error': 'No data found'}), 404

@app.route('/api/kusonime')
def api_kusonime():
    """API endpoint for Kusonime JSON"""
    data = load_json('kusonime.json')
    if data:
        return jsonify(data)
    return jsonify({'error': 'No data found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
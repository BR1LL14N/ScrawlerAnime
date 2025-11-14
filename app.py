from flask import Flask, render_template, jsonify, request, redirect, url_for, session
import json
import os
from scraper import AnimeScraper
from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'  # Change this in production
scraper = AnimeScraper()

# Simple admin authentication
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'  # Change this in production

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

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
        pages = request.args.get('pages', 2, type=int)
        result = scraper.scrape_parallel(max_pages_per_site=pages)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/scrape-otakudesu')
def scrape_otakudesu():
    """Scrape OtakuDesu only"""
    try:
        pages = request.args.get('pages', 2, type=int)
        result = scraper.scrape_otakudesu(max_pages=pages)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/scrape-kusonime')
def scrape_kusonime():
    """Scrape Kusonime only"""
    try:
        pages = request.args.get('pages', 2, type=int)
        result = scraper.scrape_kusonime(max_pages=pages)
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

@app.route('/merged')
def view_merged():
    """View merged anime data"""
    merged = load_json('merged.json')
    return render_template('merged.html', data=merged)

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

@app.route('/api/merged')
def api_merged():
    """API endpoint for merged JSON"""
    data = load_json('merged.json')
    if data:
        return jsonify(data)
    return jsonify({'error': 'No data found'}), 404

# Admin routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin_login.html', error='Invalid credentials')
    
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.pop('logged_in', None)
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin_dashboard():
    """Admin dashboard"""
    # Get all history
    all_history = scraper.get_history(limit=50)
    otaku_history = scraper.get_history('otakudesu', limit=10)
    kuso_history = scraper.get_history('kusonime', limit=10)
    
    # Get current data
    otakudesu = load_json('otakudesu.json')
    kusonime = load_json('kusonime.json')
    merged = load_json('merged.json')
    
    stats = {
        'total_scrapes': len(all_history),
        'otakudesu_count': otakudesu.get('count', 0) if otakudesu else 0,
        'kusonime_count': kusonime.get('count', 0) if kusonime else 0,
        'merged_matches': len(merged.get('matches', [])) if merged else 0,
        'last_scrape': all_history[0]['timestamp'] if all_history else 'Never'
    }
    
    return render_template('admin_dashboard.html', 
                         stats=stats, 
                         history=all_history[:20],
                         otaku_history=otaku_history,
                         kuso_history=kuso_history)

@app.route('/admin/history/<filename>')
@login_required
def view_history_file(filename):
    """View specific history file"""
    try:
        with open(f'history/{filename}', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404

@app.route('/admin/delete-history/<filename>', methods=['POST'])
@login_required
def delete_history_file(filename):
    """Delete specific history file"""
    try:
        os.remove(f'history/{filename}')
        return jsonify({'success': True, 'message': 'File deleted'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/admin/clear-history', methods=['POST'])
@login_required
def clear_history():
    """Clear all history files"""
    try:
        for filename in os.listdir('history'):
            if filename.endswith('.json'):
                os.remove(f'history/{filename}')
        return jsonify({'success': True, 'message': 'All history cleared'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
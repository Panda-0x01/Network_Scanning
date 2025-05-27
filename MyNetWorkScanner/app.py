#!/usr/bin/env python3
"""
Network Scanner Tool - Flask Application
"""

from flask import Flask, render_template, request, jsonify # type: ignore
from scanner import NetworkScanner
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize scanner
scanner = NetworkScanner()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    try:
        url = request.form.get('url', '').strip()
        port_range = request.form.get('portRange', '').strip()
        scan_type = request.form.get('scanType', 'quick')
        
        if not url:
            return jsonify({'error': 'URL is required'})
        
        # Perform scan
        quick_scan = scan_type == 'quick'
        results = scanner.scan_url(url, port_range if port_range else None, quick_scan)
        
        return jsonify(results)
        
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    print("🔍 Network Scanner Tool Starting...")
    print("📡 Server will be available at: http://localhost:5000")
    print("🌐 Open your browser and navigate to the URL above")
    print("⚡ Press Ctrl+C to stop the server")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
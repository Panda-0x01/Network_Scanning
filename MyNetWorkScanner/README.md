# Network Scanner Tool

A professional network reconnaissance tool with Flask web interface for port scanning, service detection, and HTTP analysis.

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![Flask](https://img.shields.io/badge/flask-v2.3+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Features

- **Port Scanning**: Multi-threaded scanning with configurable port ranges
- **Service Detection**: Automatic identification of running services
- **HTTP Analysis**: Header extraction, status codes, and page titles
- **Web Interface**: Modern responsive dashboard with real-time results
- **Host Discovery**: ICMP ping testing for reachability assessment

## Installation

```bash
git clone <repository-url>
cd network_scanner
pip install -r requirements.txt
python app.py
```

Open `http://localhost:5000` in your browser.

## Usage

### Web Interface
1. Enter target URL, hostname, or IP address
2. Configure port range (optional): `80`, `1-1000`, `80,443`
3. Select scan type: Quick (common ports) or Full (1-1000)
4. Click "Start Scan" to execute

### Programmatic Usage
```python
from scanner import NetworkScanner

scanner = NetworkScanner()
results = scanner.scan_url('example.com', port_range='1-100', quick_scan=False)
```

## Project Structure

```
network_scanner/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── config.py                   # Configuration settings
├── README.md                   # Project documentation
├── scanner/
│   ├── __init__.py            # Scanner package initialization
│   ├── core.py                # Core scanning functionality
│   ├── services.py            # Service detection logic
│   └── utils.py               # Utility functions
├── templates/
│   └── index.html             # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css          # CSS styles
│   ├── js/
│   │   └── main.js            # JavaScript functionality
│   └── images/
│       └── favicon.ico        # Favicon
├── tests/
│   ├── __init__.py
│   ├── test_scanner.py        # Scanner tests
│   └── test_app.py            # Flask app tests
└── logs/
    └── scanner.log            # Application logs
```

## Configuration

Edit `config.py` to customize:

```python
class Config:
    DEFAULT_TIMEOUT = 3
    MAX_THREADS = 50
    COMMON_PORTS = [21, 22, 23, 25, 53, 80, 443, 993, 995, 3389]
```

## Testing

```bash
python -m unittest discover tests/
```

## Security & Ethics

- Only scan systems you own or have explicit permission to test
- Comply with local laws and regulations
- Use for legitimate security assessments only
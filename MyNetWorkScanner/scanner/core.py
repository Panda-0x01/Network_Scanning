#!/usr/bin/env python3
"""
Core Network Scanner functionality
"""

import socket
import threading
import json
import time
import subprocess
import os
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

from .services import ServiceDetector
from .utils import NetworkUtils
from config import Config


class NetworkScanner:
    def __init__(self):
        self.config = Config()
        self.service_detector = ServiceDetector()
        self.utils = NetworkUtils()
        self.results = {}
        
    def extract_host_from_url(self, url):
        """Extract hostname from URL"""
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        parsed = urllib.parse.urlparse(url)
        return parsed.hostname or parsed.netloc
    
    def resolve_hostname(self, hostname):
        """Resolve hostname to IP address"""
        try:
            ip = socket.gethostbyname(hostname)
            return ip
        except socket.gaierror:
            return None
    
    def scan_port(self, host, port, timeout=None):
        """Scan a single port"""
        if timeout is None:
            timeout = self.config.DEFAULT_TIMEOUT
            
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return port if result == 0 else None
        except:
            return None
    
    def ping_host(self, host):
        """Ping host to check if it's alive"""
        try:
            if os.name == 'nt':  # Windows
                cmd = ['ping', '-n', '1', '-w', '3000', host]
            else:  # Unix/Linux
                cmd = ['ping', '-c', '1', '-W', '3', host]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except:
            return False
    
    def scan_url(self, url, port_range=None, quick_scan=True):
        """Main scanning function"""
        start_time = time.time()
        
        # Extract hostname
        hostname = self.extract_host_from_url(url)
        if not hostname:
            return {'error': 'Invalid URL or hostname'}
        
        # Resolve IP
        ip = self.resolve_hostname(hostname)
        if not ip:
            return {'error': 'Could not resolve hostname'}
        
        results = {
            'url': url,
            'hostname': hostname,
            'ip': ip,
            'scan_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'open_ports': [],
            'closed_ports': [],
            'http_info': {},
            'ping': False
        }
        
        # Ping test
        results['ping'] = self.ping_host(ip)
        
        # Get HTTP info if it's a web URL
        if url.startswith(('http://', 'https://')) or ':80' in url or ':443' in url:
            results['http_info'] = self.utils.get_http_info(url)
        
        # Port scanning
        ports_to_scan = self._get_ports_to_scan(port_range, quick_scan)
        
        # Scan ports using threading
        max_threads = self.config.MAX_THREADS if quick_scan else self.config.MAX_THREADS_FULL_SCAN
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            future_to_port = {
                executor.submit(self.scan_port, ip, port): port 
                for port in ports_to_scan
            }
            
            for future in as_completed(future_to_port):
                port = future_to_port[future]
                try:
                    result = future.result()
                    if result:
                        service = self.service_detector.detect_service(ip, port)
                        results['open_ports'].append({
                            'port': port,
                            'service': service
                        })
                    else:
                        results['closed_ports'].append(port)
                except:
                    results['closed_ports'].append(port)
        
        # Sort results
        results['open_ports'].sort(key=lambda x: x['port'])
        results['closed_ports'].sort()
        
        results['scan_duration'] = round(time.time() - start_time, 2)
        results['total_ports_scanned'] = len(ports_to_scan)
        
        return results
    
    def _get_ports_to_scan(self, port_range, quick_scan):
        """Determine which ports to scan"""
        if port_range:
            try:
                if '-' in port_range:
                    start_port, end_port = map(int, port_range.split('-'))
                    return range(start_port, end_port + 1)
                else:
                    return [int(port_range)]
            except:
                return self.config.COMMON_PORTS
        else:
            return self.config.COMMON_PORTS if quick_scan else range(1, 1001)
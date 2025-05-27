"""
Service Detection Module
"""

import socket
from config import Config


class ServiceDetector:
    def __init__(self):
        self.config = Config()
    
    def detect_service(self, host, port):
        """Detect service running on port"""
        service = self.config.SERVICE_MAPPINGS.get(port, "Unknown")
        
        # Try to grab banner for more info
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((host, port))
            
            if port in [80, 8080]:
                sock.send(b"GET / HTTP/1.1\r\nHost: " + host.encode() + b"\r\n\r\n")
            elif port == 443:
                service += " (SSL/TLS)"
            else:
                sock.send(b"\r\n")
            
            banner = sock.recv(1024).decode('utf-8', errors='ignore')
            sock.close()
            
            if banner and len(banner.strip()) > 0:
                service += f" - {banner[:50]}..." if len(banner) > 50 else f" - {banner.strip()}"
                
        except:
            pass
            
        return service
import os

class Config:
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    DEBUG = True
    
    # Scanner Configuration
    DEFAULT_TIMEOUT = 3
    MAX_THREADS = 50
    MAX_THREADS_FULL_SCAN = 100
    
    # Common ports for quick scan
    COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 443, 993, 995, 1723, 3389, 5900, 8080]
    
    # Service mappings
    SERVICE_MAPPINGS = {
        21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
        53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
        443: "HTTPS", 993: "IMAPS", 995: "POP3S",
        1723: "PPTP", 3389: "RDP", 5900: "VNC", 8080: "HTTP-Alt"
    }
"""
Utility functions for network scanning
"""

import requests
import re


class NetworkUtils:
    @staticmethod
    def get_http_info(url):
        """Get HTTP headers and basic info"""
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            
            response = requests.get(url, timeout=10, allow_redirects=True)
            
            info = {
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'title': '',
                'server': response.headers.get('Server', 'Unknown'),
                'content_length': len(response.content)
            }
            
            # Extract title
            title_match = re.search(r'<title[^>]*>(.*?)</title>', response.text, re.IGNORECASE | re.DOTALL)
            if title_match:
                info['title'] = title_match.group(1).strip()
            
            return info
        except Exception as e:
            return {'error': str(e)}
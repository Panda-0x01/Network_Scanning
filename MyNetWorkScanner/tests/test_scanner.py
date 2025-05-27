"""
Unit tests for Network Scanner
"""

import unittest
from scanner.core import NetworkScanner


class TestNetworkScanner(unittest.TestCase):
    def setUp(self):
        self.scanner = NetworkScanner()
    
    def test_extract_host_from_url(self):
        self.assertEqual(self.scanner.extract_host_from_url('google.com'), 'google.com')
        self.assertEqual(self.scanner.extract_host_from_url('https://google.com'), 'google.com')
        self.assertEqual(self.scanner.extract_host_from_url('http://example.com:8080'), 'example.com')
    
    def test_resolve_hostname(self):
        ip = self.scanner.resolve_hostname('google.com')
        self.assertIsNotNone(ip)
        self.assertTrue(ip.count('.') == 3)  # Basic IP format check

if __name__ == '__main__':
    unittest.main()
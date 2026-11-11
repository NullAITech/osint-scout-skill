#!/usr/bin/env python3
"""
Domain Intel OSINT Scout - Sovereign Local Server & REST API
Port: 8085
Engineered by 1nc0gn30 (@1nc0gn30) • NullAI Platform
"""

import sys
import os
import json
import time
import socket
import argparse
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse
import urllib.request

START_TIME = time.time()
PUBLIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'public')

class OSINTScoutHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=PUBLIC_DIR, **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path in ('/health', '/api/health'):
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            payload = {
                "status": "healthy",
                "service": "osint-scout-skill",
                "tool": "Domain Intel OSINT Scout",
                "port": 8085,
                "uptime_seconds": round(time.time() - START_TIME, 2),
                "license": "100% Free & Open Access",
                "support": {
                    "stripe_coffee": "https://buy.stripe.com/3cIfZg27PdKo2D64Ocfw40X"
                }
            }
            self.wfile.write(json.dumps(payload, indent=2).encode('utf-8'))
            return

        if path == '/api/recon':
            query = urllib.parse.parse_qs(parsed.query)
            domain = query.get('domain', [''])[0].strip().lower()
            if not domain:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "domain query parameter required"}).encode('utf-8'))
                return

            # Passive resolution using standard library socket
            results = {
                "target": domain,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "records": {},
                "status": "success"
            }

            try:
                # Resolve IPv4
                addr_info = socket.getaddrinfo(domain, 80, socket.AF_INET, socket.SOCK_STREAM)
                ips = sorted(list(set(item[4][0] for item in addr_info)))
                results["records"]["A"] = ips
            except Exception as e:
                results["records"]["A"] = []

            try:
                # Resolve IPv6
                addr_info6 = socket.getaddrinfo(domain, 80, socket.AF_INET6, socket.SOCK_STREAM)
                ips6 = sorted(list(set(item[4][0] for item in addr_info6)))
                results["records"]["AAAA"] = ips6
            except Exception:
                results["records"]["AAAA"] = []

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(results, indent=2).encode('utf-8'))
            return

        return super().do_GET()

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def main():
    parser = argparse.ArgumentParser(description="Domain Intel OSINT Scout Server")
    parser.add_argument('--port', type=int, default=8085, help='Port to bind (default: 8085)')
    parser.add_argument('--host', type=str, default='127.0.0.1', help='Host to bind (default: 127.0.0.1)')
    args = parser.parse_args()

    server_address = (args.host, args.port)
    httpd = HTTPServer(server_address, OSINTScoutHandler)
    print(f"✦ Domain Intel OSINT Scout running at http://{args.host}:{args.port}")
    print(f"✦ Endpoints: /health, /api/recon?domain=<domain>")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping OSINT Scout server.")
        httpd.server_close()

if __name__ == '__main__':
    main()

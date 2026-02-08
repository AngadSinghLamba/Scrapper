#!/usr/bin/env python3
"""
Simple HTTP server to serve the dashboard and handle API requests
"""

import http.server
import socketserver
import json
import os
import sys
from urllib.parse import urlparse, parse_qs

# Add tools directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tools'))
from storage_manager import load_articles, update_saved_status

PORT = 8000


class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler for dashboard API endpoints"""
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        
        # Serve dashboard HTML
        if parsed_path.path == '/' or parsed_path.path == '/index.html':
            self.path = '/dashboard.html'
            return super().do_GET()
        
        # API: Get articles
        if parsed_path.path == '/api/articles':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            data = load_articles()
            self.wfile.write(json.dumps(data).encode())
            return
        
        # Serve static files
        return super().do_GET()
    
    def do_POST(self):
        """Handle POST requests"""
        parsed_path = urlparse(self.path)
        
        # API: Toggle save status
        if parsed_path.path.startswith('/api/articles/') and parsed_path.path.endswith('/save'):
            # Extract article ID from path
            parts = parsed_path.path.split('/')
            article_id = parts[3]
            
            # Read request body
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = json.loads(body.decode())
            
            saved = data.get('saved', False)
            
            # Update saved status
            success = update_saved_status(article_id, saved)
            
            if success:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'success': True}).encode())
            else:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Article not found'}).encode())
            
            return
        
        # Default 404
        self.send_response(404)
        self.end_headers()
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests (CORS preflight)"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()


def run_server():
    """Start the dashboard server"""
    # Change to project directory
    os.chdir(os.path.dirname(__file__))
    
    with socketserver.TCPServer(("", PORT), DashboardHandler) as httpd:
        print("=" * 60)
        print("🚀 AI News Dashboard Server")
        print("=" * 60)
        print(f"Server running at: http://localhost:{PORT}")
        print(f"Dashboard URL: http://localhost:{PORT}/")
        print()
        print("Press Ctrl+C to stop the server")
        print("=" * 60)
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 Server stopped")


if __name__ == "__main__":
    run_server()

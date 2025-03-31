from http.server import BaseHTTPRequestHandler
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Read the HTML template
        template_path = os.path.join(os.path.dirname(__file__), 'templates', 'index.html')
        try:
            with open(template_path, 'r') as f:
                html_content = f.read()
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html_content.encode())
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(str(f'{{"error": "{str(e)}"}}').encode()) 
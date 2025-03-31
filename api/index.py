from http.server import BaseHTTPRequestHandler
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Get the absolute path to the template
            current_dir = os.path.dirname(os.path.abspath(__file__))
            template_path = os.path.join(current_dir, 'templates', 'index.html')
            
            # Check if file exists
            if not os.path.exists(template_path):
                raise FileNotFoundError(f"Template not found at {template_path}")
            
            # Read the HTML template
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
            error_message = f'{{"error": "Failed to load template: {str(e)}"}}'
            self.wfile.write(error_message.encode()) 
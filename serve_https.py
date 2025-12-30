"""
HTTPS Server for Medical Assistant
Enables microphone access on phone
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import ssl
import os

# Certificate files
cert_file = '10.152.119.140.pem'
key_file = '10.152.119.140-key.pem'

# Check if certificates exist
if not os.path.exists(cert_file) or not os.path.exists(key_file):
    print("❌ Certificate files not found!")
    print("Run: python generate_cert.py")
    exit(1)

class MyHTTPSHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Serve index.html
        if self.path == '/' or self.path == '/index.html':
            try:
                with open('index.html', 'rb') as f:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html; charset=utf-8')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(f.read())
            except FileNotFoundError:
                self.send_error(404, "index.html not found")
        else:
            self.send_error(404, "File not found")
    
    def log_message(self, format, *args):
        # Custom log format
        print(f"📱 {self.address_string()} - {format % args}")

# Create SSL context
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(cert_file, key_file)

# Create server
server_address = ('0.0.0.0', 8080)
httpd = HTTPServer(server_address, MyHTTPSHandler)
httpd.socket = ssl_context.wrap_socket(httpd.socket, server_side=True)

print("\n" + "="*70)
print("🔒 HTTPS SERVER STARTED - MICROPHONE ENABLED")
print("="*70)
print(f"✅ URL: https://10.152.119.140:8080/index.html")
print(f"✅ Certificate: {cert_file}")
print(f"✅ Private Key: {key_file}")
print(f"✅ Status: Running")
print("\n📱 ON YOUR PHONE:")
print("   1. Open: https://10.152.119.140:8080/index.html")
print("   2. Click 'Advanced' if you see security warning")
print("   3. Click 'Proceed to 10.152.119.140 (unsafe)'")
print("   4. Grant microphone permission when asked")
print("\n⏹️  Press Ctrl+C to stop server")
print("="*70 + "\n")

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("\n✅ Server stopped")
    httpd.server_close()

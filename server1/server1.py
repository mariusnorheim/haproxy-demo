from http.server import BaseHTTPRequestHandler, HTTPServer

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"<h1>Response from Server 1</h1>")

if __name__ == "__main__":
    server = HTTPServer(('0.0.0.0', 8081), SimpleHandler)
    print("Server 1 is running on port 8081...")
    server.serve_forever()

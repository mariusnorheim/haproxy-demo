from http.server import BaseHTTPRequestHandler, HTTPServer

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"<h1>Response from Server 2</h1>")

if __name__ == "__main__":
    server = HTTPServer(('0.0.0.0', 8082), SimpleHandler)
    print("Server 2 is running on port 8082...")
    server.serve_forever()

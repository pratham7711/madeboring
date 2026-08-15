import base64, http.server, pathlib, re

OUT = pathlib.Path(__file__).parent / 'frames'
OUT.mkdir(exist_ok=True)


class H(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        n = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(n).decode()
        idx = re.search(r'/frame/(\d+)', self.path).group(1)
        data = body.split(',', 1)[1] if ',' in body else body
        (OUT / ('f%04d.png' % int(idx))).write_bytes(base64.b64decode(data))
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.end_headers()

    def log_message(self, *a):
        pass


http.server.HTTPServer(('127.0.0.1', 4900), H).serve_forever()

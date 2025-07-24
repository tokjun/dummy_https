#!/usr/bin/env python3


# To create pem file
# openssl req -new -newkey rsa:4096 -nodes -keyout snakeoil.key -out snakeoil.csr
# openssl x509 -req -sha256 -days 365 -in snakeoil.csr -signkey snakeoil.key -out snakeoil.pem


import http.server
import http.cookiejar
import io
import socket
from http import HTTPStatus

import ssl
import os
import zlib

hostname = 'localhost'
local_ip = socket.gethostbyname(hostname)
local_port = 7787

server_address = (local_ip, local_port)

print(f"Open https://{hostname}:{local_port}/samples/idengine_sample_wasm/sample.html")
print(f'Open https://{local_ip}:{local_port}/samples/idengine_sample_wasm/sample.html')

class CORSHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {
        '': 'application/octet-stream',
        '.manifest': 'text/cache-manifest',
        '.html': 'text/html',
        '.png': 'image/png',
        '.jpg': 'image/jpg',
        '.svg':	'image/svg+xml',
        '.css':	'text/css',
        '.js': 'application/x-javascript',
        '.wasm': 'application/wasm',
        '.json': 'application/json',
        '.xml': 'application/xml',
    }

    def do_GET(self):
        """Serve a GET request."""
        if f := self.send_reply():
            try:
                if hasattr(f, "read"):
                    self.copyfile(f, self.wfile)
                else:
                    for data in f:
                        self.wfile.write(data)
            finally:
                f.close()

    def do_POST(self):
        """Serve a POST request."""
        if f := self.send_reply():
            try:
                if hasattr(f, "read"):
                    self.copyfile(f, self.wfile)
                else:
                    for data in f:
                        self.wfile.write(data)
            finally:
                f.close()

    def send_reply(self):
        # The server send back a template.html regardless of the requested path.
        path = self.translate_path(self.path)
        f = None
        try:
            if self.path == '/SRC/v2/product/authorization/register':
                f = open('templates/registration_response.json', 'rb')
            else:
                f = open('templates/default.html', 'rb')
        except OSError:
            self.send_error(HTTPStatus.NOT_FOUND, "File not found")
            return None

        ctype = self.guess_type('templates/template.html')

        #print("Request: ", self.path)

        try:
            fs = os.fstat(f.fileno())
            content_length = fs[6]
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-type", ctype)
            self.send_header("Content-Length", str(content_length))
            self.end_headers()
            return f
        except:
            f.close()
            raise

    def end_headers(self):
        # Include additional response headers here. CORS for example:
        self.send_header('Access-Control-Allow-Origin', '*')
        http.server.SimpleHTTPRequestHandler.end_headers(self)


httpd = http.server.ThreadingHTTPServer(server_address, CORSHTTPRequestHandler)
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.check_hostname = False
ctx.load_cert_chain(certfile='dummy.pem', keyfile='dummy.key', password=None)  # with key inside
httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)
httpd.serve_forever()

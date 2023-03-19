import requests
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

import config
from waf import BlockedRequest


def PassWafToHandler(waf):
    # built for every http request
    class ProxyHTTPRequestHandler(BaseHTTPRequestHandler):
        protocol_version = 'HTTP/1.0'

        def __init__(self, *args,  **kwargs):
            self.waf_impl = waf
            super().__init__(*args, **kwargs)

        def do_GET(self):
            try:
                # For example - http://127.0.0.1:65413/users | http://127.0.0.1:65413/users?user=10
                url = 'http://{}:{}{}'.format(config.hostname,
                                              config.port, self.path)

                req_header = self.parse_headers()
                req_header['Host'] = config.hostname  # 127.0.0.1
                body = parse_qs(urlparse(url).query)
                self.waf_impl.validate_req(
                    self.client_address[0], body, url, req_header)

                resp = requests.get(url, headers=req_header, verify=False)

                self.send_response(resp.status_code)
                self.send_resp_headers(resp)
                self.wfile.write(resp.text.encode(
                    encoding='UTF-8', errors='strict'))

            except BlockedRequest as e:
                self.send_error(
                    404, 'error trying to proxy - forbidden request')

        def do_POST(self):
            try:
                # https://google.com/post?parm1=x&parm2=y
                url = 'http://{}:{}{}'.format(config.hostname,
                                              config.port, self.path)
                req_header = self.parse_headers()
                req_header['Host'] = config.hostname
                body = parse_qs(urlparse(url).query)
                self.waf_impl.validate_req(
                    self.client_address[0], body, url, req_header)

                resp = requests.post(url, headers=req_header, verify=False)

                self.send_response(resp.status_code)
                self.send_resp_headers(resp)
                self.wfile.write(resp.text.encode(
                    encoding='UTF-8', errors='strict'))

            except BlockedRequest as e:
                self.send_error(
                    404, 'error trying to proxy - forbidden request')

        def parse_headers(self):
            req_header = {}
            for key in self.headers.keys():
                req_header[key] = self.headers[key]

            return req_header

        def send_resp_headers(self, resp):
            for key in resp.headers:
                # Added by default
                if key not in ['Content-Encoding', 'Transfer-Encoding', 'content-encoding', 'transfer-encoding',
                               'content-length', 'Content-Length']:
                    self.send_header(key, resp.headers[key])
            self.send_header('Content-Length', str(len(resp.content)))
            self.end_headers()

    return ProxyHTTPRequestHandler

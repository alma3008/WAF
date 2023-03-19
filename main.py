import waf
import HttpProxyServer
from http.server import HTTPServer

import URLPhishingValidator


def main():
    # waf-ip:waf-port
    server_address = ('0.0.0.0', 1234)
    waf_server = HTTPServer(server_address, HttpProxyServer.PassWafToHandler(waf.WAF()))
    waf_server.serve_forever()  # starts the waf server


if __name__ == '__main__':
    main()

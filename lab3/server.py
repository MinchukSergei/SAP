from http.server import CGIHTTPRequestHandler, HTTPServer
from init_db import init


def run(server_class=HTTPServer, handler_class=CGIHTTPRequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()


if __name__ == '__main__':
    from sys import argv

    init()
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()

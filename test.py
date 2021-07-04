import random
import time
import http.server
from prometheus_client import start_http_server
from prometheus_client import Counter
from prometheus_client import Gauge
from prometheus_client import Summary

REQUESTS = Counter('hello_worlds_total',
                   'Hello Worlds requested.')
EXCEPTIONS = Counter('hello_world_exceptions_total',
                     'Exceptions serving Hello World.')

INPROGRESS = Gauge('hello_worlds_inprogress',
                   'Number of Hello Worlds in progress.')
LAST = Gauge('hello_world_last_time_seconds',
             'The last time a Hello World was served.')
TIME = Gauge('time_seconds', 'The current time.')

#  specify a function to be called at exposition time
TIME.set_function(lambda: time.time())

LATENCY = Summary('hello_world_latency_seconds',
                  'Time for a request Hello World.')


class MyHandler(http.server.BaseHTTPRequestHandler):
    @LATENCY.time()
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello World")


if __name__ == "__main__":
    print("restarting server")
    start_http_server(8000)
    server = http.server.HTTPServer(('localhost', 8001), MyHandler)
    server.serve_forever()

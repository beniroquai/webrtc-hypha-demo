import os
from http.server import HTTPServer, CGIHTTPRequestHandler
server_object = HTTPServer(server_address=('0.0.0.0', 88), RequestHandlerClass=CGIHTTPRequestHandler)
server_object.serve_forever()

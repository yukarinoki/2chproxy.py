from http.server import BaseHTTPRequestHandler, HTTPServer, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse
import urllib.request
import logging
import socket
import threading
import select
import makedat

address = ('127.0.0.1', 8080)

def transfer(dest_file, src_file):
    dest_file.write(src_file.read())

class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print('path = {}'.format(self.path))

        parsed_path = urlparse(self.path)
        print('parsed: path = {}, query = {}'.format(parsed_path.path, parse_qs(parsed_path.query)))
        print('headers\r\n-----\r\n{}-----'.format(self.headers))

        cgiurl = makedat.daturl2cgiurl(self.path)
        logging.info(cgiurl)
        dat = makedat.scraping(cgiurl)
       
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; charset=shift_jis')
        self.end_headers()
        self.wfile.write(dat.encode('shift_jis', errors="replace"))

    def do_POST(self):
        print('path = {}'.format(self.path))

        parsed_path = urlparse(self.path)
        print('parsed: path = {}, query = {}'.format(parsed_path.path, parse_qs(parsed_path.query)))

        print('headers\r\n-----\r\n{}-----'.format(self.headers))

        content_length = int(self.headers['content-length'])
        
        print('body = {}'.format(self.rfile.read(content_length).decode('utf-8')))
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(b'Hello from do_POST')

    def do_CONNECT(self):
        logging.info('path = {}'.format(self.path))

        parsed_path = urlparse(self.path)
        # print('parsed: path = {}, query = {}'.format(parsed_path.path, parse_qs(parsed_path.query)))
        logging.info('headers\r\n-----\r\n{}-----'.format(self.headers))
        host, port = self.headers["host"].split(":")
        logging.info(host, int(port))

        dest_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try :
            dest_conn.connect((host, int(port)))
        except Exception as e:
            print(e)

        self.protocol_version="HTTP/1.1"
        self.send_response(200)
        self.end_headers()

        poll = select.poll()
        poll.register(dest_conn, select.POLLIN)
        poll.register(self.rfile, select.POLLIN)

        fin = False
        while True:
            rdy = poll.poll()
            for fno, ev in rdy:
                if fno == self.rfile.fileno():
                    if ev == select.POLLIN:
                        data = self.rfile.read1(8192)
                        print(data)
                        dest_conn.send(data)
                    else:
                        fin = True
                if fno == dest_conn.fileno():
                    if ev == select.POLLIN:
                        data = dest_conn.recv(8192)
                        self.wfile.write(data)
                    else:
                        fin = True
            if fin:
                break    
        dest_conn.close()
        return


with HTTPServer(address, MyHTTPRequestHandler) as server:
    server.serve_forever()
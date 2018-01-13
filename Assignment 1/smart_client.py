# University of Victoria
# Spring 2018
# CSC 361 Assignment 1
# Michael Reiter
# V00831568

import argparse
import re
import socket
import ssl
import sys
from urllib.parse import urlparse

class Cookie:
    def __init__(self, name, key, domain_name):
        self.name = name
        self.key = key
        self.domain_name = domain_name
    
    def __str__(self):
        return "name: " + self.name + ", key: " + self.key + ", domain name: " + self.domain_name

def perform_http(uri):
    # Try to resolve host's IP address from URI
    try:
        ip_address = socket.gethostbyname(uri)
    except socket.gaierror:
        print("Error resolving host. Exiting.")
        sys.exit()

    # Try to create socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print("Error creating socket. Exiting.")
        sys.exit()

    # Try to connect using HTTPS
    try:
        ssl_context = ssl.create_default_context()

        # Try to set application protocols
        try:
            protocols = ["h2", "http/1.1", "http/1.0"]
            ssl_context.set_alpn_protocols(protocols)
        except NotImplementedError:
            print("OpenSSL version error. Verify that Python 3 is being used.")

        ssl_s = ssl.wrap_socket(s)
        connect_and_send_message(s=ssl_s, ip_address=ip_address, use_https=True)

    except ssl.SSLError:
        # HTTPS failed, thus host is using HTTP
        connect_and_send_message(s=s, ip_address=ip_address, use_https=False)             

    ssl_s.close()

def connect_and_send_message(s, ip_address, use_https):
    if use_https:
        port = 443
    else:
        port = 80

    s.connect((ip_address, port))

    # Try to use HTTP/1.1
    status_code, response = send_request(s=s, request=b"GET / HTTP/1.1\r\n\r\n")
    if status_code == 200:
        # Success
        print("200 OK")
    elif status_code == 400:
        # Bad Request. Try to use HTTP/1.0
        status_code, response = send_request(s=s, request=b"GET / HTTP/1.0\r\n\r\n")

def send_request(s, request):
    # Try to send request
    try:
        s.sendall(request)

        # s.setblocking(False)
        while True:
            response = s.recv(1024*(2**5))
            if response:
                status_code = int(re.search(r"^(HTTP/1.[0|1])\s(\d+)", response.decode()).group(2))
                return status_code, response.decode()
            else:
                print('No response')
                pass

    except socket.error:
        print("Error sending request. Exiting.")
        sys.exit()

def main():
    # parser = argparse.ArgumentParser()
    # parser.add_argument("uri")
    # args = parser.parse_args()
    # uri = args.uri
    unparsed_uri = "http://web.uvic.ca"
    parsed_uri = urlparse(unparsed_uri)
    uri = parsed_uri.netloc
    print("website: " + uri)
    perform_http(uri)
    supports_https = "not implemented"
    http_version = "not implemented"
    cookies = [Cookie("-", "asdf", "test.com")]
    print("1. Support of HTTPS: " + supports_https)
    print("2. The newest HTTP versions that the web server supports: " + http_version)
    print("3. List of Cookies:")
    for cookie in cookies:
        print(cookie)

if __name__ == "__main__":
    main()

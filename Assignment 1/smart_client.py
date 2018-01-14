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

DEBUG_PRINT_ENABLED = True

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

    http_version = "undetermined"
    # Try to use HTTP/1.1
    status_code, response = send_request(
        ip_address=ip_address,
        request=b"GET / HTTP/1.1\r\n\r\n",
        use_https=True
    )
    if status_code == 200:
        # Success
        if DEBUG_PRINT_ENABLED:
            print("HTTP/1.1 returned 200 OK")
        http_version = "HTTP/1.1"
    elif status_code == 302:
        # Try again with https
        if DEBUG_PRINT_ENABLED:
            print("HTTP/1.1 returned 302 Found")            
    elif status_code == 400:
        # Bad Request. Try to use HTTP/1.0
        if DEBUG_PRINT_ENABLED:
            print("HTTP/1.1 returned 400 Bad Request")        
        status_code, response = send_request(
            ip_address=ip_address,
            request=b"GET / HTTP/1.0\r\n\r\n",
            use_https=True
        )
        if status_code == 200:
            # Success
            if DEBUG_PRINT_ENABLED:
                print("HTTP/1.0 returned 200 OK")            
            http_version = "HTTP/1.0"
        elif status_code == 400:
            if DEBUG_PRINT_ENABLED:
                print("HTTP/1.0 returned 400 Bad Request")
        else:
            if DEBUG_PRINT_ENABLED:
                print("HTTP/1.0 returned unexpected status code " + str(status_code))
    else:
        if DEBUG_PRINT_ENABLED:
            print("HTTP/1.1 returned unexpected status code " + str(status_code))
    
    return "not implemented", http_version, [Cookie("-", "asdf", "test.com")]


def send_request(ip_address, request, use_https):
    if use_https:
        port = 443
    else:
        port = 80

    s = create_socket(use_https=use_https)
    s.connect((ip_address, port))

    # Try to send request
    try:
        if DEBUG_PRINT_ENABLED:
            print("Sent request " + str(request) + " to " + ip_address + ":" + str(port) + " with use HTTPS " + str(use_https))
        s.sendall(request)
        # s.setblocking(False)
        while True:
            response = s.recv(1024*(2**5))
            if response:
                if DEBUG_PRINT_ENABLED:
                    print(response.decode())
                status_code = int(re.search(r"^(HTTP/1.[0|1])\s(\d+)", response.decode()).group(2))
                return status_code, response.decode()
            else:
                if DEBUG_PRINT_ENABLED:
                    print('No response')
                pass

    except socket.error:
        print("Error sending request. Exiting.")
        sys.exit()


def create_socket(use_https):
    # Try to create socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print("Error creating socket. Exiting.")
        sys.exit()

    if use_https:
        # Try to connect using HTTPS
        try:
            ssl_context = ssl.create_default_context()
            # Try to set application protocols
            try:
                protocols = ["h2", "http/1.1", "http/1.0"]
                ssl_context.set_alpn_protocols(protocols)
            except NotImplementedError:
                print("OpenSSL version error. Verify that Python 3 is being used.")
            s = ssl.wrap_socket(s)
        except ssl.SSLError:
            print("SSL error. Exiting.")
            sys.exit()

    return s


def main():
    # parser = argparse.ArgumentParser()
    # parser.add_argument("uri")
    # args = parser.parse_args()
    # uri = args.uri
    # unparsed_uri = "http://web.uvic.ca"
    # unparsed_uri = "https://hannahbishop.com"
    unparsed_uri = "http://www.uvic.ca"
    parsed_uri = urlparse(unparsed_uri)
    uri = parsed_uri.netloc
    print("website: " + uri)
    supports_https, http_version, cookies = perform_http(uri)
    print("1. Support of HTTPS: " + supports_https)
    print("2. The newest HTTP versions that the web server supports: " + http_version)
    print("3. List of Cookies:")
    for cookie in cookies:
        print(cookie)


if __name__ == "__main__":
    main()

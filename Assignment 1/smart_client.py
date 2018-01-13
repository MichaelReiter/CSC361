# University of Victoria
# Spring 2018
# CSC 361 Assignment 1
# Michael Reiter
# V00831568

import argparse
import socket
import ssl
import sys
from urllib.parse import urlparse

def print_request():
    request = None
    header = None
    request_body = None

    print("---Request begin---")
    print(request)
    print("Host: ")
    print("Connection: Keep-Alive") # part of header?
    print("\n")
    print("---Request end---")
    print("HTTP request sent, awaiting response...")
    print("\n")
    print("---Response header---")
    print(header) # and cookies
    print("\n")
    print("---Response body---")
    print(request_body)

def main():
    # parser = argparse.ArgumentParser()
    # parser.add_argument("uri")
    # args = parser.parse_args()
    # uri = args.uri
    unparsed_uri = "http://web.uvic.ca"
    parsed_uri = urlparse(unparsed_uri)
    uri = parsed_uri.netloc

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
        connected_msg = "Connected to " + ip_address + " using HTTPS"
    else:
        port = 80
        connected_msg = "Connected to " + ip_address + " using HTTP"

    s.connect((ip_address, port))
    print(connected_msg)

    # Try to send request
    try:
        request = b"GET / HTTP/1.1\r\n\r\n"
        s.sendall(request)
        print("Sent request: " + str(request))

        # s.setblocking(False)
        while True:
            response = s.recv(1024*(2**5))
            if response:
                print(response)
                # print(response.decode()[0:100])
            else:
                break

    except socket.error:
        print("Error sending request. Exiting.")
        sys.exit()

if __name__ == "__main__":
    main()

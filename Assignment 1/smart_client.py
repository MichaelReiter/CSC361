# University of Victoria
# Spring 2018
# CSC 361 Assignment 1
# Michael Reiter
# V00831568

import argparse
import socket
import ssl

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

def socket_stuff(uri):
    # Try to resolve host's IP address from URI
    try:
        ip_address = socket.gethostbyname(uri)
    except socket.gaierror as gaie:
        # Could not resolve host, so exit
        print(gaie)
        sys.exit()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Try to connect using HTTPS
    try:
        ssl_context = ssl.create_default_context()

        try:
            protocols = ["h2", "http/1.1", "http/1.0"]
            ssl_context.set_alpn_protocols(protocols)
        except NotImplementedError as nie:
            # OpenSSL version error. Verify that Python 3 is being used.
            print(nie)

        ssl_s = ssl.wrap_socket(s, )
        ssl_s.connect((ip_address, 443))
        
        # request = b"HEAD https://uvic.ca\r\n\r\n"
        request = b"GET / HTTP/1.0\r\n\r\n"
        ssl_s.send(request)

        while True:
            response = ssl_s.recv(4096)
            print(response)
            # break

    except ssl.SSLError as e:
        # HTTPS failed, thus host is using HTTP
        print(e)

    ssl_s.close()

def main():
    # parser = argparse.ArgumentParser()
    # parser.add_argument("uri")
    # args = parser.parse_args()
    # socket_stuff(args.uri)
    socket_stuff("www.uvic.ca")

if __name__ == "__main__":
    main()

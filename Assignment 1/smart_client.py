# University of Victoria
# Spring 2018
# CSC 361 Assignment 1
# Michael Reiter
# V00831568

import argparse
import socket
import ssl
import sys

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
        ssl_s.connect((ip_address, 443))

        # Try to send message
        try:
            message = b"GET / HTTP/1.1\r\n\r\n"
            ssl_s.sendall(message)
            response = ssl_s.recv(1024)
            
            while True:
                response = ssl_s.recv(1024)
                if response:
                    print(response.decode())
                else:
                    break

            # while True:
            #     response = ssl_s.recv(1024)
                # print(response)
        except socket.error:
            print("Error sending message. Exiting.")
            sys.exit()

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

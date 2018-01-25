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

class Cookie:
    '''
    Cookie parsed from HTTP response header has name, key and domain.
    '''
    def __init__(self, name, key, domain_name):
        self.name = name
        self.key = key
        self.domain_name = domain_name

        if self.name is None:
            self.name = ""

        if self.key is None:
            self.key = ""

        if self.domain_name is None:
            self.domain_name = ""

    def __str__(self):
        return "name: " + self.name + ", key: " + self.key + ", domain name: " + self.domain_name


def create_socket_and_connect(url, use_https):
    '''
    Creates a new socket and connects to url optionally using HTTPS.
    Returns created socket.
    '''
    # Try to create socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print("Error creating socket. Exiting.")
        sys.exit()

    # Try to resolve host IP from url
    try:
        ip_address = socket.gethostbyname(url)
    except socket.gaierror:
        print("Error resolving host. Exiting.")
        sys.exit()

    if use_https:
        port = 443
    else:
        port = 80

    # Try to connect on secure port
    try:
        sock.connect((ip_address, port))
    except socket.error:
        raise Exception

    if use_https:
        # Try to wrap socket
        try:
            # ssl_context = ssl.create_default_context()
            sock = ssl.wrap_socket(sock)
        except ssl.SSLError:
            raise Exception

    return sock


def send_request(sock, request):
    '''
    Send an HTTP request through a socket.
    Returns (status code, http_version, response).
    '''
    try:
        sock.sendall(request)
    except socket.error:
        raise Exception

    # Try to receive response
    data = b""
    response = b""
    status_code = -1
    while True:
        try:
            data = sock.recv(4096)
            if not data:
                break
            response += data
            if status_code == -1:
                regex = re.search(r"^(HTTP/1.[0|1])\s(\d+)", response.decode())
                http_version = regex.group(1)
                status_code = int(regex.group(2))
        except socket.timeout:
            break

    return status_code, http_version, response


def perform_http(url):
    '''
    Determines if HTTPS is supported, protocol version supported and parses cookies
    Returns (supports_https, newest_http_version, cookies)
    '''
    supports_https = "undetermined"
    newest_http_version = "undetermined"
    cookies = []

    # Try to create a secure socket
    try:
        sock = create_socket_and_connect(url, use_https=True)
    except Exception:
        supports_https = "no"

    # Try to send HTTP/1.1 GET request
    try:
        http_1_0_request = ("HEAD / HTTP/1.0\r\n\r\n").encode()
        http_1_1_request = ("HEAD / HTTP/1.1\r\nHost: " + url + "\r\n\r\n").encode()
        status_code, http_version, response = send_request(
            sock,
            request=http_1_1_request
        )
    except Exception:
        print("Failed HTTP/1.1")

    if status_code in [301, 302]:
        new_location = re.search(r"Location: (\w+)://(.+)/", response.decode())
        redirect_protocol = new_location.group(1)
        new_url = new_location.group(2)
        print("Status code: " + str(status_code) + ". Redirected to " + redirect_protocol + "://" + new_url)
        if redirect_protocol == "http":
            new_sock = create_socket_and_connect(new_url, use_https=False)
            new_status_code, new_http_version, new_response = send_request(
                sock=new_sock,
                request=http_1_1_request
            )
            if new_status_code in [200, 404, 505]:
                newest_http_version = new_http_version
                supports_https = "no"

        if redirect_protocol == "https":
            new_sock = create_socket_and_connect(new_url, use_https=True)
            new_status_code, new_http_version, new_response = send_request(
                sock=new_sock,
                request=http_1_1_request
            )
            if new_status_code in [200, 404, 505]:
                newest_http_version = new_http_version
                supports_https = "yes"
    elif status_code in [200, 404, 505]:
        newest_http_version = http_version
        supports_https = "yes"
    else:
        print("Terminated due to unexpected status code: " + str(status_code))
        sys.exit()

    if check_http2_support(url):
        newest_http_version = "HTTP/2"

    cookies = parse_cookies(str(response))

    return supports_https, newest_http_version, cookies


def check_http2_support(url):
    '''
    Checks if a URL supports HTTP/2 protocol.
    Returns True or False.
    '''
    ctx = ssl.create_default_context()
    ctx.set_alpn_protocols(['h2', 'spdy/3', 'http/1.1'])
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn = ctx.wrap_socket(sock, server_hostname=url)
    conn.connect((url, 443))
    return conn.selected_alpn_protocol() == "h2"


def parse_cookies(response):
    '''
    Parses cookies from a url.
    Returns a list of Cookies.
    '''
    matches = re.finditer(r"Set-Cookie: (.+)=(.+); ((path)=(.+);)? ((domain)=(.+))?", response)
    cookies = []
    for match in matches:
        key = match.group(1)
        domain = match.group(8)
        cookies.append(Cookie("-", key, domain))
    return cookies


def main():
    '''
    Determines whether a web server supports HTTPS,
    the newest supported verion of HTTP and parses
    cookies.
    '''
    socket.setdefaulttimeout(3)
    # parser = argparse.ArgumentParser()
    # parser.add_argument("url")
    # args = parser.parse_args()
    # url = args.url

    # url = "www.cbc.ca"
    # url = "www.uvic.ca"
    # url = "www.google.ca"
    # url = "www.mcgill.ca"
    # url = "www.youtube.com"
    # url = "www.akamai.com"
    # url = "www2.gov.bc.ca"
    # url = "www.python.org"
    # url = "www.aircanada.com" # error
    url = "www.bbc.com"
    print("website: " + url)
    supports_https, newest_http_version, cookies = perform_http(url)
    print("1. Support of HTTPS: " + supports_https)
    print("2. The newest HTTP versions that the web server supports: " + newest_http_version)
    print("3. List of Cookies:")
    for cookie in cookies:
        print(cookie)


if __name__ == "__main__":
    main()

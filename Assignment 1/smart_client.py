"""
University of Victoria
Spring 2018
CSC 361 Assignment 1
Michael Reiter
V00831568
"""

import argparse
import re
import socket
import ssl
import sys
from typing import List
from urllib.parse import urlparse

MAX_REDIRECTS = 5

class Cookie:
    """
    Cookie parsed from HTTP response header has name, key and domain.
    """
    def __init__(self, name: str, key: str, domain_name: str) -> None:
        self.name: str = name
        self.key: str = key
        self.domain_name: str = domain_name

    def __str__(self) -> str:
        return f"name: {self.name}, key: {self.key}, domain name: {self.domain_name}"


def create_socket_and_connect(url: str, use_https: bool) -> socket.socket:
    """
    Creates a new socket and connects to url optionally using HTTPS.
    Returns created socket.
    """
    # Try to create socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print("Error creating socket. Exiting.")
        sys.exit()

    if use_https:
        port = 443
    else:
        port = 80

    # Try to connect on secure port
    try:
        sock.connect((url, port))
    except socket.error:
        raise Exception

    if use_https:
        # Try to wrap socket
        try:
            sock = ssl.wrap_socket(sock)
        except ssl.SSLError:
            raise Exception

    return sock


def send_request(url: str, path: str, version: str, use_https: bool) -> str:
    """
    Sends an HTTP request to provided url.
    Returns response string.
    """
    sock = create_socket_and_connect(url, use_https)
    request = (f"HEAD {path} HTTP/{version}\r\nHost: {url}\r\n\r\n").encode()
    sock.sendall(request)
    response = b""
    while True:
        try:
            data = sock.recv(4096)
            if not data:
                break
            response += data
        except socket.timeout:
            break
    return response.decode("utf-8")


def parse_cookies(url: str, response: str) -> List[Cookie]:
    """
    Parses cookies from a url.
    Returns a list of Cookies.
    """
    cookies = []
    for match in re.findall(r"Set-Cookie: (.*?)=(.*?);.* (domain=(.*))?", response):
        d = re.search(r".*?(\..*)", url).group(1)
        if match[3] == "":
            domain = d
        else:
            domain = match[3]
        cookies.append(Cookie("-", match[0], domain))
    return cookies


def check_http2_support(url: str) -> bool:
    """
    Checks if a URL supports HTTP/2 protocol.
    Returns True or False.
    """
    context = ssl.create_default_context()
    context.set_alpn_protocols(['h2', 'spdy/3', 'http/1.1'])
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    secure_sock = context.wrap_socket(sock, server_hostname=url)
    secure_sock.connect((url, 443))
    return secure_sock.selected_alpn_protocol() == "h2"


def get_status_code(response: str) -> int:
    """
    Parses a status code from a HTTP response.
    Returns status code as an integer.
    """
    return int(re.search(r"^(HTTP/1.[0|1])\s(\d+)", response).group(2))


def get_http_version(url: str, response: str) -> str:
    """
    Parses a HTTP version from a HTTP response.
    Returns string indicating protocol version.
    """
    version = re.search(r"^(HTTP/1.[0|1])\s(\d+)", response).group(1)

    if check_http2_support(url):
        version = "HTTP/2"

    return version


def check_if_supports_https(url: str) -> str:
    """
    Determines if HTTPS is supported.
    Returns "yes" or "no"
    """
    location = url
    path = "/"
    i = 0
    while i < MAX_REDIRECTS:
        response = send_request(location, path, "1.1", use_https=True)
        status_code = get_status_code(response)
        if status_code in [200, 404, 503, 505]:
            return "yes", response
        elif status_code in [301, 302]:
            i += 1
            new_location = urlparse(re.search(r"Location: (.*)", response).group(1))
            location = new_location.netloc
            path = new_location.path
            print(f"Redirected to {new_location.scheme}://{location}")
            if new_location.scheme == "http":
                return "no", response
        else:
            print(f"Exiting due to unexpected status code: {status_code}. Please try rerunning.")
            sys.exit()


def main() -> None:
    """
    Determines whether a web server supports HTTPS,
    the newest supported verion of HTTP and parses
    cookies.
    """
    socket.setdefaulttimeout(3)
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    args = parser.parse_args()
    url = args.url
    print(f"website: {url}")
    supports_https, response = check_if_supports_https(url)
    newest_http_version = get_http_version(url, response)
    cookies = parse_cookies(url, response)
    print(f"1. Support of HTTPS: {supports_https}")
    print(f"2. The newest HTTP versions that the web server supports: {newest_http_version}")
    print("3. List of Cookies:")
    for cookie in cookies:
        print(cookie)


if __name__ == "__main__":
    main()

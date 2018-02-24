#!/usr/bin/env python3
"""
University of Victoria
Spring 2018
CSC 361 Assignment 1
Michael Reiter
V00831568
"""

import argparse
import socket
from http.cookies import Cookie, parse_cookies
from http.requests import check_if_supports_https, get_http_version
from typing import List

def main() -> None:
    """
    Determines whether a web server supports HTTPS,
    the newest supported verion of HTTP and parses
    cookies.
    """
    socket.setdefaulttimeout(3)
    parser: argparse.ArgumentParser() = argparse.ArgumentParser()
    parser.add_argument("url")
    args: argparse.Namespace = parser.parse_args()
    url: str = args.url
    print(f"website: {url}")
    supports_https, response = check_if_supports_https(url)
    newest_http_version: str = get_http_version(url, response)
    cookies: List[Cookie] = parse_cookies(url, response)
    print(f"1. Support of HTTPS: {supports_https}")
    print(f"2. The newest HTTP versions that the web server supports: {newest_http_version}")
    print("3. List of Cookies:")
    for cookie in cookies:
        print(cookie)

if __name__ == "__main__":
    main()

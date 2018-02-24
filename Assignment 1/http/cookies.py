import re
from typing import List

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

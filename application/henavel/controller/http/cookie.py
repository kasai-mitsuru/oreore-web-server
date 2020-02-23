from datetime import datetime, timedelta
from typing import Dict, Iterable


class Cookie:
    def __init__(
        self,
        name: str,
        value: str,
        domain: str = "",
        path: str = "",
        max_age: int = -1,
        secure: bool = False,
        http_only: bool = True,
    ):
        self.name: str = name
        self.value: str = value
        self.domain: str = domain
        self.path: str = path
        self.max_age: int = max_age
        self.secure: bool = secure
        self.http_only: bool = http_only

    def update(
        self,
        name: str = None,
        value: str = None,
        domain: str = None,
        path: str = None,
        max_age: int = None,
        secure: bool = False,
        http_only: bool = True,
    ):
        if name is not None:
            self.name = name
        if value is not None:
            self.value = value
        if domain is not None:
            self.domain = domain
        if path is not None:
            self.path = path
        if max_age is not None:
            self.max_age = max_age
        if secure is not None:
            self.secure = secure
        if http_only is not None:
            self.http_only = http_only

    def get_header_format(self):
        items = [f"{self.name}={self.value}"]

        if self.domain:
            items.append(f"Domain={self.domain}")
        if self.path:
            items.append(f"Path={self.path}")
        if self.max_age > -1:
            expires = (datetime.now() + timedelta(seconds=self.max_age)).strftime(
                "%a, %d %b %Y %H:%M:%S GMT"
            )
            items.append(f"Expires={expires}")
        if self.secure:
            items.append("Secure")
        if self.http_only:
            items.append("HttpOnly")

        return "; ".join(items)


class CookieContainer:
    def __init__(self, cookies: Iterable[Cookie] = None):
        if cookies is None:
            cookies = []

        self.cookies: Dict[str, Cookie] = {cookie.name: cookie for cookie in cookies}

    def __iter__(self):
        return (cookie for cookie in self.cookies.values())

    def save(self, cookie: Cookie) -> "CookieContainer":
        self.cookies[cookie.name] = cookie
        return self

    def update(self, name: str, *args, **kwargs):
        if name in self.cookies:
            self.cookies[name].update(*args, **kwargs)
        else:
            raise KeyError(f"a cookie '{name}' does not exist.")

    def remove(self, name: str) -> "CookieContainer":
        if name in self.cookies:
            del self.cookies[name]
        return self

    def get(self, name, default=None):
        if name in self.cookies:
            return self.cookies[name]
        else:
            if default is None:
                raise KeyError(f"a cookie '{name}' does not exist.")
            else:
                return default

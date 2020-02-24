from datetime import datetime
from typing import Dict, Iterable, Union


class Cookie:
    EXPIRES_FORMAT = "%a, %d %b %Y %H:%M:%S GMT"

    def __init__(
        self,
        name: str,
        value: str,
        domain: str = None,
        path: str = None,
        expires: datetime = None,
        max_age: int = None,
        secure: bool = False,
        http_only: bool = True,
    ):
        self.name: str = name
        self.value: str = value
        self.domain: Union[str, None] = domain
        self.path: Union[str, None] = path
        self.expires: Union[datetime, None] = expires
        self.max_age: Union[int, None] = max_age
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

        if self.domain is not None:
            items.append(f"Domain={self.domain}")
        if self.path is not None:
            items.append(f"Path={self.path}")
        if self.expires is not None:
            expires = self.expires.strftime(self.EXPIRES_FORMAT)
            items.append(f"Expires={expires}")
        if self.max_age is not None:
            items.append(f"Max-Age={str(self.max_age)}")
        if self.secure:
            items.append("Secure")
        if self.http_only:
            items.append("HttpOnly")

        return "; ".join(items)

    def is_expired(self):
        return self.expires < datetime.now()


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

    def get(self, name, default=None, raises=False):
        if name in self.cookies:
            return self.cookies[name]
        else:
            if raises is True:
                raise KeyError(f"a cookie '{name}' does not exist.")
            else:
                return default

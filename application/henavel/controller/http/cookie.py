from datetime import datetime, timedelta


class Cookie:
    def __init__(
        self,
        name: str = "",
        value: str = "",
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

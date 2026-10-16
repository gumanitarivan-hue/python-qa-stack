import requests


class ApiClient(requests.Session):
    """Сессия requests с базовым URL и таймаутом по умолчанию."""

    def __init__(self, base_url: str, timeout: int = 10):
        super().__init__()
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def request(self, method, url, **kwargs):
        kwargs.setdefault("timeout", self.timeout)
        return super().request(method, f"{self.base_url}{url}", **kwargs)

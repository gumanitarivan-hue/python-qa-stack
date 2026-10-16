import pytest

from src.api.client import ApiClient

API_URL = "https://jsonplaceholder.typicode.com"


@pytest.fixture(scope="session")
def api():
    with ApiClient(API_URL) as client:
        yield client

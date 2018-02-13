
from architect_client.libarchitect import ArchitectClient


def test_class_url():
    test_url = 'http://test.url'
    client = ArchitectClient(test_url)
    assert test_url == client.api_url

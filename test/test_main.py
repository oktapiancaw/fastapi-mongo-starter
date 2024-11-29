from fastapi.testclient import TestClient

from src.main import app


client = TestClient(app)


def test_service_status():
    """
    Check if the service status is ok.

    The service status is assumed to be ok if a GET request to the root URL
    returns a 200 status code.
    """
    response = client.get("/")
    assert response.status_code == 200

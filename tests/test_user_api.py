# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.error import Error  # noqa: F401
from openapi_server.models.user import User  # noqa: F401


def test_create_user(client: TestClient):
    """Test case for create_user

    Create user
    """
    user = {"first_name":"firstName","last_name":"lastName","phone":"phone","id":0,"email":"email","username":"username"}

    headers = {
    }
    response = client.request(
        "POST",
        "/user",
        headers=headers,
        json=user,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_delete_user(client: TestClient):
    """Test case for delete_user

    
    """

    headers = {
    }
    response = client.request(
        "DELETE",
        "/user/{userId}".format(userId=56),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_find_user_by_id(client: TestClient):
    """Test case for find_user_by_id

    
    """

    headers = {
    }
    response = client.request(
        "GET",
        "/user/{userId}".format(userId=56),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_update_user(client: TestClient):
    """Test case for update_user

    
    """
    user = {"first_name":"firstName","last_name":"lastName","phone":"phone","id":0,"email":"email","username":"username"}

    headers = {
    }
    response = client.request(
        "PUT",
        "/user/{userId}".format(userId=56),
        headers=headers,
        json=user,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


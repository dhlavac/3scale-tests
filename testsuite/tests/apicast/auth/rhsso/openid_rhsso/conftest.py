"""
Conftest for the openid rhsso credentials locations tests
"""

import pytest
from pytest_cases import fixture_plus


@fixture_plus(scope="module")
def api_client(api_client):
    """
    Staging client
    The auth of the session is set up to none in order to test different auth methods
    The auth of the request will be passed in test functions
    """
    # pylint: disable=protected-access
    api_client._session.auth = None
    return api_client


# Used for parametrize_plus, because normal fixture doesn't work with @parametrize_plus
@fixture_plus(scope="module")
def production_client(prod_client):
    """
    Production client
    The auth of the session is set up to none in order to test different auth methods
    The auth of the request will be passed in test functions
    """
    client = prod_client()
    # pylint: disable=protected-access
    client._session.auth = None
    return client


@pytest.fixture
def token(application, rhsso_service_info):
    """Access token for 3scale application that is connected with RHSSO"""
    app_key = application.keys.list()["keys"][0]["key"]["value"]
    return rhsso_service_info.password_authorize(application["client_id"], app_key).token['access_token']
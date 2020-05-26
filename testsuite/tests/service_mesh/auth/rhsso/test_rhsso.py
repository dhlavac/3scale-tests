"""
Testing service authentication using OIDC with RHSSO
"""
import pytest
from threescale_api.resources import Service

from testsuite.gateways.gateways import Capability

pytestmark = pytest.mark.required_capabilities(Capability.SERVICE_MESH)


def test_rhsso_auth(api_client, service):
    """Check if OIDC connect using RHSSO works"""
    response = api_client.get("/get")
    assert response.status_code == 200
    assert service["backend_version"] == Service.AUTH_OIDC
    assert response.request.headers["Authorization"].startswith("Bearer")


def test_rhsso_no_auth(application):
    """Check if OIDC connect without auth won't work"""
    client = application.api_client()
    # pylint: disable=protected-access
    client._session.auth = None
    response = client.get("/get")

    assert response.status_code == 401

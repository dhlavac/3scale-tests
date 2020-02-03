"""
A policy that allows you to reject incoming requests with a specified status code and message.
This policy should override others and reject all requests.
Expected: to return specified code eg 328 and message of service unavailability.
Issue: https://issues.jboss.org/browse/THREESCALE-3189
"""

import pytest
from testsuite import rawobj


@pytest.fixture(scope="module")
def policy_settings():
    """Have service with maintenance_mode policy added and configured to return custom message and code"""

    return rawobj.PolicyConfig("maintenance_mode", {
        "message_content_type": "text/plain; charset=utf-8",
        "status": 328,
        "message": "Service Unavailable - Maintenance"})


def test_maintenance_mode_policy(testconfig, application):
    """Test request to service with maintenance_mode set returns appropriate message and status code"""

    response = application.test_request(verify=testconfig["ssl_verify"])
    assert response.status_code == 328
    assert response.text == "Service Unavailable - Maintenance\n"

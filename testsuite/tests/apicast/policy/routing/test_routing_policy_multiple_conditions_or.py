"""
Rewrite spec/functional_specs/policies/routing/routing_with_multiple_conditions_or_spec.rb
"""
from urllib.parse import urlparse
import pytest
from testsuite import rawobj
from testsuite.echoed_request import EchoedRequest


@pytest.fixture(scope="module")
def service(service, backend):
    """Set policy settings"""
    test_header1 = {"op": "==", "value": "route", "match": "header", "header_name": "Test1"}
    test_header2 = {"op": "matches", "value": "test", "match": "header", "header_name": "Test2"}
    proxy = service.proxy.list()
    proxy.policies.insert(0, rawobj.PolicyConfig("routing", {"rules": [
        {"url": backend("echo-api") + "/route",
         "condition": {
             "combine_op": "or",
             "operations": [test_header1, test_header2]}}]}))
    return service


def test_routing_policy_route_testing(api_client, backend):
    """
    Test for the request send with Test1 and Test2 to echo/route/get
    """
    parsed_url = urlparse(backend("echo-api"))
    response = api_client.get("/get", headers={"Test1": "route", "Test2": "testing"})
    assert response.status_code == 200
    echoed_request = EchoedRequest.create(response)
    assert echoed_request.path == "/route/get"
    assert echoed_request.headers["Host"] == parsed_url.hostname
    assert echoed_request.headers["Test1"] == "route"
    assert echoed_request.headers["Test2"] == "testing"


def test_routing_policy_route_hello(api_client, backend):
    """
    Test for the request send with Test1 valid and Test2 invalid value to echo api
    """
    parsed_url = urlparse(backend("echo-api"))
    response = api_client.get("/get", headers={"Test1": "route", "Test2": "hello"})
    assert response.status_code == 200
    echoed_request = EchoedRequest.create(response)
    assert echoed_request.path == "/route/get"
    assert echoed_request.headers["Host"] == parsed_url.hostname
    assert echoed_request.headers["Test1"] == "route"
    assert echoed_request.headers["Test2"] == "hello"


def test_routing_policy_noroute_test(api_client, backend):
    """
    Test for the request send with Test2 valid and Test1 invalid to echo api
    """
    parsed_url = urlparse(backend("echo-api"))
    response = api_client.get("/get", headers={"Test1": "noroute", "Test2": "test"})
    assert response.status_code == 200
    echoed_request = EchoedRequest.create(response)

    assert echoed_request.path == "/route/get"
    assert echoed_request.headers["Host"] == parsed_url.hostname
    assert echoed_request.headers["Test1"] == "noroute"
    assert echoed_request.headers["Test2"] == "test"


def test_routing_policy_route(api_client, backend):
    """
    Test for the request send without Test2 to echo api
    """
    parsed_url = urlparse(backend("echo-api"))
    response = api_client.get("/get", headers={"Test1": "route"})
    assert response.status_code == 200
    echoed_request = EchoedRequest.create(response)
    assert echoed_request.path == "/route/get"
    assert echoed_request.headers["Host"] == parsed_url.hostname
    assert echoed_request.headers["Test1"] == "route"


def test_routing_policy_empty(api_client, backend):
    """
    Test for the request send without any header to / to httpbin api
    """
    parsed_url = urlparse(backend())
    response = api_client.get("/get")
    echoed_request = EchoedRequest.create(response)
    assert response.status_code == 200
    assert echoed_request.headers["Host"] == parsed_url.hostname

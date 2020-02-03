"""
Rewrite: 3scale-amp-tests/spec/functional_specs/update_staging_spec.rb
"""


def test_updated_auth_param(application, service):
    """
    The update of the staging configuration must be propagated immediately

    Updates the user key in the staging env
    Request using the old key returns 403
    Request using the new_key returns 200
    """

    old_api_client = application.api_client()
    # change of the user key
    service.proxy.list().update(params={"auth_user_key": "new_key"})

    new_api_client = application.api_client()

    old_param_response = old_api_client.get("/anything")
    new_param_response = new_api_client.get("/anything")

    assert old_param_response.status_code == 403
    assert new_param_response.status_code == 200

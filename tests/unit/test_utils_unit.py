"""Unit tests for the utils module."""

import pytest

from pagerduty_mcp_server import utils

@pytest.mark.unit
@pytest.mark.utils
def test_api_response_handler_single_result():
    """Test that api_response_handler formats a single result correctly."""
    result = {'id': '123', 'name': 'test'}
    response = utils.api_response_handler(
        results=result,
        resource_name='test'
    )

    assert response == {
        'metadata': {
            'count': 1,
            'description': 'Found 1 result for resource type test'
        },
        'test': [result]
    }

@pytest.mark.unit
@pytest.mark.utils
def test_api_response_handler_multiple_results():
    """Test that api_response_handler formats multiple results correctly."""
    results = [
        {'id': '123', 'name': 'test1'},
        {'id': '456', 'name': 'test2'}
    ]
    response = utils.api_response_handler(
        results=results,
        resource_name='tests'
    )

    assert response == {
        'metadata': {
            'count': 2,
            'description': 'Found 2 results for resource type tests'
        },
        'tests': results
    }

@pytest.mark.unit
@pytest.mark.utils
def test_api_response_handler_with_metadata():
    """Test that api_response_handler includes additional metadata."""
    result = {'id': '123', 'name': 'test'}
    additional_metadata = {'status': 'active'}
    response = utils.api_response_handler(
        results=result,
        resource_name='test',
        additional_metadata=additional_metadata
    )

    assert response['metadata']['status'] == 'active'

@pytest.mark.unit
@pytest.mark.utils
def test_api_response_handler_limit_exceeded():
    """Test that api_response_handler handles limit exceeded correctly."""
    results = [{'id': str(i)} for i in range(utils.RESPONSE_LIMIT + 50)]
    response = utils.api_response_handler(
        results=results,
        resource_name='tests',
        limit=utils.RESPONSE_LIMIT
    )

    assert 'error' in response
    assert response['error']['code'] == 'LIMIT_EXCEEDED'
    assert f'exceeds the limit of {utils.RESPONSE_LIMIT}' in response['error']['message']

@pytest.mark.unit
@pytest.mark.utils
def test_api_response_handler_empty_resource_name():
    """Test that api_response_handler raises ValidationError for empty resource_name."""
    with pytest.raises(utils.ValidationError) as exc_info:
        utils.api_response_handler(
            results={'id': '123'},
            resource_name=''
        )
    assert str(exc_info.value) == "resource_name cannot be empty"

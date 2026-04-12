"""
Tests for Extract Module
"""

import os
import sys
import pytest
from unittest.mock import patch, MagicMock

# Ensure the project root is on sys.path when running this test directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.extract import fetch_football_standings


@patch('src.extract.requests.get')
def test_fetch_football_standings_success(mock_get):
    """Test successful API data fetching."""
    # Mock successful response
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        'standings': [{'table': [{'rank': 1, 'team': {'name': 'Arsenal'}}]}]
    }
    mock_get.return_value = mock_response

    result = fetch_football_standings()

    assert 'standings' in result
    mock_get.assert_called_once()


@patch('src.extract.requests.get')
def test_fetch_football_standings_http_error(mock_get):
    """Test API request failure."""
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = Exception("404 Client Error")
    mock_get.return_value = mock_response

    with pytest.raises(SystemExit):
        fetch_football_standings()
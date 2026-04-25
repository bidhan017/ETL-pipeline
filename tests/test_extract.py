"""
Tests for Extract Module
"""

import os
import sys
import pytest
from unittest.mock import patch, MagicMock

# Ensure the project root is on sys.path when running this test directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock environment variables before importing src.extract
os.environ['API_KEY'] = 'test_api_key'
os.environ['LEAGUE_CODE'] = 'PL'

from src.extract import fetch_football_standings, fetch_team_last_matches, fetch_all_recent_matches


@patch('src.extract.requests.get')
def test_fetch_football_standings_success(mock_get):
    """Test successful API data fetching."""
    # Mock successful response
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        'standings': [{'table': [{'position': 1, 'team': {'name': 'Arsenal', 'id': 1}}]}]
    }
    mock_get.return_value = mock_response

    result = fetch_football_standings()

    assert 'standings' in result
    mock_get.assert_called_once()


@patch('src.extract.requests.get')
def test_fetch_football_standings_http_error(mock_get):
    """Test API request failure raises SystemExit."""
    from requests.exceptions import HTTPError
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = HTTPError("404 Client Error")
    mock_get.return_value = mock_response

    with pytest.raises(SystemExit):
        fetch_football_standings()


@patch('src.extract.requests.get')
def test_fetch_football_standings_timeout(mock_get):
    """Test API request timeout raises SystemExit."""
    from requests.exceptions import Timeout
    mock_get.side_effect = Timeout("Request timed out")

    with pytest.raises(SystemExit):
        fetch_football_standings()


@patch('src.extract.requests.get')
def test_fetch_team_last_matches_success(mock_get):
    """Test successful team matches fetching."""
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        'matches': [
            {'score': {'fullTime': {'home': 2, 'away': 1}}},
            {'score': {'fullTime': {'home': 0, 'away': 0}}}
        ]
    }
    mock_get.return_value = mock_response

    result = fetch_team_last_matches(team_id=1, limit=5)

    assert result is not None
    assert 'matches' in result
    mock_get.assert_called_once()


@patch('src.extract.requests.get')
def test_fetch_team_last_matches_failure(mock_get):
    """Test team matches fetch failure returns None."""
    from requests.exceptions import HTTPError
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = HTTPError("500 Server Error")
    mock_get.return_value = mock_response

    result = fetch_team_last_matches(team_id=999)

    assert result is None


@patch('src.extract.requests.get')
def test_fetch_all_recent_matches_success(mock_get):
    """Test successful recent matches fetching."""
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        'matches': [{'id': 1, 'status': 'FINISHED'}]
    }
    mock_get.return_value = mock_response

    result = fetch_all_recent_matches("PL")

    assert 'matches' in result
    mock_get.assert_called_once()


@patch('src.extract.requests.get')
def test_fetch_all_recent_matches_http_error(mock_get):
    """Test recent matches fetch failure raises exception."""
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = Exception("403 Forbidden")
    mock_get.return_value = mock_response

    with pytest.raises(Exception):
        fetch_all_recent_matches("PL")
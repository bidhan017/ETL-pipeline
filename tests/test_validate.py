"""
Tests for Validate Module
"""

import os
import sys
import pandas as pd
import pytest

# Ensure the project root is on sys.path when running this test directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.validate import validate_standings_data, validate_api_response


def test_validate_standings_data_success():
    """Test validation passes with valid data."""
    df = pd.DataFrame({
        'P': [1, 2, 3],
        'Team': ['Arsenal', 'Liverpool', 'Chelsea'],
        'GP': [10, 10, 9],
        'W': [7, 6, 5],
        'D': [2, 3, 2],
        'L': [1, 1, 2],
        'F': [20, 18, 15],
        'A': [10, 8, 7],
        'GD': [10, 10, 8],
        'Pts': [23, 21, 17],
        'Form': ['WWW', 'WWL', 'DDL']
    })

    result = validate_standings_data(df)
    
    assert result is True


def test_validate_standings_data_empty():
    """Test validation fails with empty DataFrame."""
    df = pd.DataFrame()

    with pytest.raises(ValueError, match="DataFrame is empty"):
        validate_standings_data(df)


def test_validate_standings_data_missing_columns():
    """Test validation fails with missing required columns."""
    df = pd.DataFrame({
        'P': [1, 2],
        'Team': ['Arsenal', 'Liverpool']
        # Missing GP, W, D, L, F, A, GD, Pts
    })

    with pytest.raises(ValueError, match="Missing required columns"):
        validate_standings_data(df)


def test_validate_standings_data_null_values():
    """Test validation fails with null values in critical columns."""
    df = pd.DataFrame({
        'P': [1, 2, 3],
        'Team': ['Arsenal', 'Liverpool', 'Chelsea'],
        'GP': [10, None, 8],  # Null in critical column
        'W': [7, 6, 5],
        'D': [2, 3, 2],
        'L': [1, 1, 2],
        'F': [20, 18, 15],
        'A': [10, 8, 7],
        'GD': [10, 10, 8],
        'Pts': [23, 21, 17]
    })

    with pytest.raises(ValueError, match="Null values found in critical column"):
        validate_standings_data(df)


def test_validate_standings_data_invalid_position():
    """Test validation fails with invalid position values."""
    df = pd.DataFrame({
        'P': [0, 2, 3],  # Position 0 is invalid
        'Team': ['Arsenal', 'Liverpool', 'Chelsea'],
        'GP': [10, 10, 9],
        'W': [7, 6, 5],
        'D': [2, 3, 2],
        'L': [1, 1, 2],
        'F': [20, 18, 15],
        'A': [10, 8, 7],
        'GD': [10, 10, 8],
        'Pts': [23, 21, 17]
    })

    with pytest.raises(ValueError, match="Position values must be between 1 and 20"):
        validate_standings_data(df)


def test_validate_standings_data_negative_games():
    """Test validation fails with negative games played."""
    df = pd.DataFrame({
        'P': [1, 2, 3],
        'Team': ['Arsenal', 'Liverpool', 'Chelsea'],
        'GP': [-1, 10, 9],  # Negative games played
        'W': [7, 6, 5],
        'D': [2, 3, 2],
        'L': [1, 1, 2],
        'F': [20, 18, 15],
        'A': [10, 8, 7],
        'GD': [10, 10, 8],
        'Pts': [23, 21, 17]
    })

    with pytest.raises(ValueError, match="Games played must be non-negative"):
        validate_standings_data(df)


def test_validate_standings_data_goal_difference():
    """Test validation warns when GD doesn't match F - A."""
    df = pd.DataFrame({
        'P': [1, 2, 3],
        'Team': ['Arsenal', 'Liverpool', 'Chelsea'],
        'GP': [10, 10, 9],
        'W': [7, 6, 5],
        'D': [2, 3, 2],
        'L': [1, 1, 2],
        'F': [20, 18, 15],
        'A': [10, 8, 7],
        'GD': [99, 10, 8],  # Wrong GD for Arsenal
        'Pts': [23, 21, 17]
    })

    # Should not raise, but logs warning
    result = validate_standings_data(df)
    assert result is True


def test_validate_standings_data_points_calculation():
    """Test validation warns when points don't match 3*W + D."""
    df = pd.DataFrame({
        'P': [1, 2, 3],
        'Team': ['Arsenal', 'Liverpool', 'Chelsea'],
        'GP': [10, 10, 9],
        'W': [7, 6, 5],
        'D': [2, 3, 2],
        'L': [1, 1, 2],
        'F': [20, 18, 15],
        'A': [10, 8, 7],
        'GD': [10, 10, 8],
        'Pts': [99, 21, 17]  # Wrong points for Arsenal (should be 23)
    })

    # Should not raise, but logs warning
    result = validate_standings_data(df)
    assert result is True


def test_validate_api_response_success():
    """Test API response validation passes with valid data."""
    api_data = {
        'standings': [{
            'table': [
                {'position': 1, 'team': {'name': 'Arsenal'}}
            ]
        }]
    }

    result = validate_api_response(api_data)
    
    assert result is True


def test_validate_api_response_not_dict():
    """Test API response validation fails when not a dictionary."""
    api_data = "not a dictionary"

    with pytest.raises(ValueError, match="API response is not a dictionary"):
        validate_api_response(api_data)


def test_validate_api_response_missing_standings():
    """Test API response validation fails when standings key is missing."""
    api_data = {'competition': 'Premier League'}

    with pytest.raises(ValueError, match="API response missing 'standings' key"):
        validate_api_response(api_data)


def test_validate_api_response_empty_standings():
    """Test API response validation fails when standings is empty."""
    api_data = {'standings': []}

    with pytest.raises(ValueError, match="Standings data is empty"):
        validate_api_response(api_data)


def test_validate_api_response_missing_table():
    """Test API response validation fails when table key is missing."""
    api_data = {'standings': [{'group': 'League'}]}

    with pytest.raises(ValueError, match="Standings data missing 'table' key"):
        validate_api_response(api_data)
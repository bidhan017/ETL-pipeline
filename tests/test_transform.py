"""
Tests for Transform Module
"""

import os
import sys
import pandas as pd

# Ensure the project root is on sys.path when running this test directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.transform import process_standings_data, compute_form


def test_process_standings_data_with_form():
    """Test data processing from API response with matches data for form."""
    api_data = {
        'standings': [{
            'table': [{
                'position': 1,
                'team': {'name': 'Arsenal', 'id': 1},
                'playedGames': 10,
                'won': 7,
                'draw': 2,
                'lost': 1,
                'goalsFor': 20,
                'goalsAgainst': 10,
                'goalDifference': 10,
                'points': 23
            }]
        }]
    }
    
    matches_data = {
        1: [
            {'score': {'fullTime': {'home': 2, 'away': 1}}},
            {'score': {'fullTime': {'home': 1, 'away': 2}}},
            {'score': {'fullTime': {'home': 3, 'away': 0}}},
            {'score': {'fullTime': {'home': 0, 'away': 0}}},
            {'score': {'fullTime': {'home': 1, 'away': 1}}}
        ]
    }

    result = process_standings_data(api_data, matches_data)

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 1
    assert result.iloc[0]['Team'] == 'Arsenal'
    assert result.iloc[0]['Pts'] == 23
    assert list(result.columns) == ['P', 'Team', 'GP', 'W', 'D', 'L', 'F', 'A', 'GD', 'Pts', 'Form']


def test_process_standings_data_without_matches():
    """Test data processing without matches data (form should be empty string)."""
    api_data = {
        'standings': [{
            'table': [
                {
                    'position': 1,
                    'team': {'name': 'Arsenal', 'id': 1},
                    'playedGames': 10,
                    'won': 7,
                    'draw': 2,
                    'lost': 1,
                    'goalsFor': 20,
                    'goalsAgainst': 10,
                    'goalDifference': 10,
                    'points': 23
                },
                {
                    'position': 2,
                    'team': {'name': 'Liverpool', 'id': 2},
                    'playedGames': 10,
                    'won': 6,
                    'draw': 3,
                    'lost': 1,
                    'goalsFor': 18,
                    'goalsAgainst': 8,
                    'goalDifference': 10,
                    'points': 21
                }
            ]
        }]
    }

    result = process_standings_data(api_data, None)

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2
    assert list(result.columns) == ['P', 'Team', 'GP', 'W', 'D', 'L', 'F', 'A', 'GD', 'Pts', 'Form']
    assert result.iloc[0]['Team'] == 'Arsenal'
    assert result.iloc[1]['Team'] == 'Liverpool'
    # Form should be None when no matches data (empty dict from build_team_form_map)
    assert result.iloc[0]['Form'] is None


def test_process_standings_data_column_check():
    """Test that all required columns are present."""
    api_data = {
        'standings': [{
            'table': [{
                'position': 1,
                'team': {'name': 'Test Team', 'id': 1},
                'playedGames': 5,
                'won': 3,
                'draw': 1,
                'lost': 1,
                'goalsFor': 10,
                'goalsAgainst': 5,
                'goalDifference': 5,
                'points': 10
            }]
        }]
    }

    result = process_standings_data(api_data, None)
    expected_columns = ['P', 'Team', 'GP', 'W', 'D', 'L', 'F', 'A', 'GD', 'Pts', 'Form']

    assert list(result.columns) == expected_columns


def test_process_standings_data_values():
    """Test that data values are correctly mapped."""
    api_data = {
        'standings': [{
            'table': [{
                'position': 3,
                'team': {'name': 'Chelsea', 'id': 3},
                'playedGames': 8,
                'won': 5,
                'draw': 2,
                'lost': 1,
                'goalsFor': 15,
                'goalsAgainst': 7,
                'goalDifference': 8,
                'points': 17
            }]
        }]
    }

    result = process_standings_data(api_data, None)

    assert result.iloc[0]['P'] == 3
    assert result.iloc[0]['Team'] == 'Chelsea'
    assert result.iloc[0]['GP'] == 8
    assert result.iloc[0]['W'] == 5
    assert result.iloc[0]['D'] == 2
    assert result.iloc[0]['L'] == 1
    assert result.iloc[0]['F'] == 15
    assert result.iloc[0]['A'] == 7
    assert result.iloc[0]['GD'] == 8
    assert result.iloc[0]['Pts'] == 17


def test_compute_form_wins():
    """Test form computation with winning matches (home team wins)."""
    matches_data = {
        'matches': [
            {'homeTeam': {'id': 1}, 'awayTeam': {'id': 2}, 'score': {'fullTime': {'home': 2, 'away': 1}}},
            {'homeTeam': {'id': 1}, 'awayTeam': {'id': 3}, 'score': {'fullTime': {'home': 3, 'away': 0}}},
            {'homeTeam': {'id': 1}, 'awayTeam': {'id': 4}, 'score': {'fullTime': {'home': 1, 'away': 0}}}
        ]
    }

    result = compute_form(matches_data, team_id=1)
    
    assert result == 'WWW'


def test_compute_form_losses():
    """Test form computation with losing matches (team is away team and loses all)."""
    matches_data = {
        'matches': [
            {'homeTeam': {'id': 2}, 'awayTeam': {'id': 1}, 'score': {'fullTime': {'home': 2, 'away': 1}}},
            {'homeTeam': {'id': 3}, 'awayTeam': {'id': 1}, 'score': {'fullTime': {'home': 2, 'away': 1}}},
            {'homeTeam': {'id': 4}, 'awayTeam': {'id': 1}, 'score': {'fullTime': {'home': 3, 'away': 0}}}
        ]
    }

    result = compute_form(matches_data, team_id=1)
    
    assert result == 'LLL'


def test_compute_form_draws():
    """Test form computation with drawn matches."""
    matches_data = {
        'matches': [
            {'homeTeam': {'id': 1}, 'awayTeam': {'id': 2}, 'score': {'fullTime': {'home': 1, 'away': 1}}},
            {'homeTeam': {'id': 3}, 'awayTeam': {'id': 1}, 'score': {'fullTime': {'home': 0, 'away': 0}}}
        ]
    }

    result = compute_form(matches_data, team_id=1)
    
    assert result == 'DD'


def test_compute_form_empty():
    """Test form computation with empty matches."""
    result = compute_form([], team_id=1)
    
    assert result is None


def test_compute_form_none():
    """Test form computation with None matches."""
    result = compute_form(None, team_id=1)
    
    assert result is None
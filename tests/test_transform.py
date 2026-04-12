"""
Tests for Transform Module
"""

import pandas as pd
from src.transform import process_standings_data


def test_process_standings_data():
    """Test data processing from API response."""
    api_data = {
        'standings': [{
            'table': [{
                'rank': 1,
                'team': {'name': 'Arsenal'},
                'all': {
                    'played': 10,
                    'win': 7,
                    'draw': 2,
                    'lose': 1,
                    'goals': {'for': 20, 'against': 10}
                },
                'goalsDiff': 10,
                'points': 23
            }]
        }]
    }

    result = process_standings_data(api_data)

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 1
    assert result.iloc[0]['Team'] == 'Arsenal'
    assert result.iloc[0]['Pts'] == 23
    assert list(result.columns) == ['P', 'Team', 'GP', 'W', 'D', 'L', 'F', 'A', 'GD', 'Pts']
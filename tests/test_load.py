"""
Tests for Load Module
"""

import os
import sys
import pytest
from unittest.mock import patch, MagicMock, call

# Ensure the project root is on sys.path when running this test directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock environment variables before importing src.load
os.environ['MYSQL_DATABASE'] = 'test_db'
os.environ['MYSQL_USERNAME'] = 'test_user'
os.environ['MYSQL_PASSWORD'] = 'test_password'
os.environ['MYSQL_HOST'] = 'localhost'
os.environ['MYSQL_PORT'] = '3306'

from src.load import get_database_connection, create_standings_table, load_standings_data


@patch('src.load.pymysql.connect')
def test_get_database_connection_success(mock_connect):
    """Test successful database connection."""
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn

    result = get_database_connection()

    assert result == mock_conn
    mock_connect.assert_called_once()


@patch('src.load.pymysql.connect')
def test_get_database_connection_failure(mock_connect):
    """Test database connection failure raises exception."""
    from pymysql import Error
    mock_connect.side_effect = Error("Connection failed")

    with pytest.raises(Error):
        get_database_connection()


@patch('src.load.get_database_connection')
def test_create_standings_table_success(mock_get_conn):
    """Test successful table creation."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_conn.return_value = mock_conn

    create_standings_table(mock_conn)

    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_called_once()


@patch('src.load.get_database_connection')
def test_create_standings_table_failure(mock_get_conn):
    """Test table creation failure raises exception."""
    from pymysql import Error
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.execute.side_effect = Error("Table creation failed")
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_conn.return_value = mock_conn

    with pytest.raises(Error):
        create_standings_table(mock_conn)


@patch('src.load.get_database_connection')
def test_load_standings_data_success(mock_get_conn):
    """Test successful data loading."""
    import pandas as pd
    
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_conn.return_value = mock_conn

    df = pd.DataFrame({
        'P': [1, 2],
        'Team': ['Arsenal', 'Liverpool'],
        'GP': [10, 10],
        'W': [7, 6],
        'D': [2, 3],
        'L': [1, 1],
        'F': [20, 18],
        'A': [10, 8],
        'GD': [10, 10],
        'Pts': [23, 21],
        'Form': ['WWW', 'WWL']
    })

    load_standings_data(mock_conn, df)

    # Should have 2 execute calls (one for each row)
    assert mock_cursor.execute.call_count == 2
    mock_conn.commit.assert_called_once()


@patch('src.load.get_database_connection')
def test_load_standings_data_failure(mock_get_conn):
    """Test data loading failure raises exception."""
    import pandas as pd
    from pymysql import Error

    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.execute.side_effect = Error("Insert failed")
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_conn.return_value = mock_conn

    df = pd.DataFrame({
        'P': [1],
        'Team': ['Arsenal'],
        'GP': [10],
        'W': [7],
        'D': [2],
        'L': [1],
        'F': [20],
        'A': [10],
        'GD': [10],
        'Pts': [23],
        'Form': ['WWW']
    })

    with pytest.raises(Error):
        load_standings_data(mock_conn, df)


@patch('src.load.get_database_connection')
def test_load_standings_data_sql_format(mock_get_conn):
    """Test that SQL is formatted correctly with all columns."""
    import pandas as pd
    
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_conn.return_value = mock_conn

    df = pd.DataFrame({
        'P': [1],
        'Team': ['Arsenal'],
        'GP': [10],
        'W': [7],
        'D': [2],
        'L': [1],
        'F': [20],
        'A': [10],
        'GD': [10],
        'Pts': [23],
        'Form': ['WWW']
    })

    load_standings_data(mock_conn, df)

    # Get the SQL that was executed
    call_args = mock_cursor.execute.call_args
    sql_query = call_args[0][0]
    
    # Verify SQL contains all expected columns
    assert 'position' in sql_query
    assert 'team' in sql_query
    assert 'games_played' in sql_query
    assert 'wins' in sql_query
    assert 'draws' in sql_query
    assert 'losses' in sql_query
    assert 'goals_for' in sql_query
    assert 'goals_against' in sql_query
    assert 'goal_difference' in sql_query
    assert 'points' in sql_query
    assert 'form' in sql_query
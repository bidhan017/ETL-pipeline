"""
Validate Module

This module handles data validation and quality checks.
"""

import logging
import pandas as pd

# Get logger
logger = logging.getLogger(__name__)


def validate_standings_data(df):
    """
    Validate the standings DataFrame for data quality.

    Args:
        df (pd.DataFrame): Standings DataFrame to validate

    Returns:
        bool: True if validation passes, False otherwise

    Raises:
        ValueError: If validation fails
    """
    logger.info("Validating standings data")

    # Check if DataFrame is empty
    if df.empty:
        raise ValueError("DataFrame is empty")

    # Check required columns exist
    required_columns = ['P', 'Team', 'GP', 'W', 'D', 'L', 'F', 'A', 'GD', 'Pts']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    # Check for null values in critical columns
    critical_columns = ['P', 'Team', 'GP', 'Pts']
    for col in critical_columns:
        if df[col].isnull().any():
            raise ValueError(f"Null values found in critical column: {col}")

    # Check position values are valid (1-20 for Premier League)
    if not all(df['P'].between(1, 20)):
        raise ValueError("Position values must be between 1 and 20")

    # Check games played is reasonable
    if not all(df['GP'] >= 0):
        raise ValueError("Games played must be non-negative")

    # Check goal difference calculation: GD = F - A
    expected_gd = df['F'] - df['A']
    if not (df['GD'] == expected_gd).all():
        logger.warning("Goal difference doesn't match F - A calculation")

    # Check points calculation: roughly 3*W + D
    expected_points = 3 * df['W'] + df['D']
    if not (df['Pts'] == expected_points).all():
        logger.warning("Points don't match 3*W + D calculation")

    logger.info("Data validation passed")
    return True


def validate_api_response(api_data):
    """
    Validate the API response structure.

    Args:
        api_data (dict): Raw API response data

    Returns:
        bool: True if validation passes

    Raises:
        ValueError: If API response is invalid
    """
    logger.info("Validating API response")

    if not isinstance(api_data, dict):
        raise ValueError("API response is not a dictionary")

    if 'standings' not in api_data:
        raise ValueError("API response missing 'standings' key")

    if not api_data['standings']:
        raise ValueError("Standings data is empty")

    if 'table' not in api_data['standings'][0]:
        raise ValueError("Standings data missing 'table' key")

    logger.info("API response validation passed")
    return True</content>
<parameter name="filePath">c:\Users\bchan\Desktop\TUD\project\python_sql_football_data_pipeline\src\validate.py
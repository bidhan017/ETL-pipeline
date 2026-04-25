"""
This script orchestrates the ETL pipeline for football data:
Extract -> Transform -> Validate -> Load
"""

import logging
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from extract import fetch_football_standings, fetch_all_recent_matches
from transform import process_standings_data, display_standings
from validate import validate_api_response, validate_standings_data
from load import (
    get_database_connection, create_standings_table,
    load_standings_data, create_ranked_view
)

LEAGUE_CODE = os.getenv("LEAGUE_CODE", "PL")

# Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('football_table_standings.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def main():
    """
    Main ETL pipeline execution.
    """
    logger.info("Starting Football Data Pipeline")

    try:
        # Extract
        logger.info("Step 1: Extracting data")
        api_data = fetch_football_standings()
        matches_data = fetch_all_recent_matches(LEAGUE_CODE)

        #print("Raw API Data:")
        #print(api_data)

        # Validate API response
        validate_api_response(api_data)

        # Transform
        logger.info("Step 2: Transforming data")
        standings_df = process_standings_data(api_data, matches_data)

        # Validate transformed data
        validate_standings_data(standings_df)

        # Display results
        display_standings(standings_df)

        # Load
        logger.info("Step 3: Loading data to database")
        connection = get_database_connection()

        create_standings_table(connection)
        load_standings_data(connection, standings_df)
        create_ranked_view(connection)

        connection.close()

        logger.info("Pipeline completed successfully")

    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
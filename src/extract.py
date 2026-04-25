import os
import logging
import requests
from requests.exceptions import HTTPError, RequestException, Timeout
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
API_KEY = os.getenv("API_KEY")
LEAGUE_CODE = os.getenv("LEAGUE_CODE", "PL")

# Get logger
logger = logging.getLogger(__name__)


def fetch_football_standings():
    """
    Fetch Premier League standings data from football-data.org API.

    Returns:
        dict: JSON response containing standings data

    Raises:
        SystemExit: If API request fails
    """

    # API Request Configuration
    url = f"https://api.football-data.org/v4/competitions/{LEAGUE_CODE}/standings"
   
    headers = {"X-Auth-Token": API_KEY}
    query_string = {}

    logger.info(f"Fetching data from {url}")

    # Make API request with error handling
    try:
        api_response = requests.get(url, headers=headers, params=query_string, timeout=15)
        api_response.raise_for_status()
        logger.info("Successfully fetched data from API")

    except HTTPError as http_err:
        logger.error(f'HTTP error occurred: {http_err}')
        raise SystemExit(1)

    except Timeout:
        logger.error('Request timed out after 15 seconds')
        raise SystemExit(1)

    except RequestException as request_err:
        logger.error(f'Request error occurred: {request_err}')
        raise SystemExit(1)

    return api_response.json()

def fetch_team_last_matches(team_id, limit=5):
    """
    Fetch last N finished matches for a given team.

    Args:
        team_id (int): Team ID from API
        limit (int): Number of matches (default 5)

    Returns:
        dict: JSON response with match data
    """

    url = f"https://api.football-data.org/v4/teams/{team_id}/matches"
    headers = {"X-Auth-Token": API_KEY}
    params = {
        "status": "FINISHED",
        "limit": limit
    }

    logger.info(f"Fetching last {limit} matches for team {team_id}")

    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        response.raise_for_status()
        return response.json()

    except (HTTPError, Timeout, RequestException) as e:
        logger.error(f"Error fetching matches for team {team_id}: {e}")
        return None  # don’t kill whole pipeline
    
def fetch_all_recent_matches(LEAGUE_CODE):
    url = f"https://api.football-data.org/v4/competitions/{LEAGUE_CODE}/matches"

    headers = {"X-Auth-Token": API_KEY}
    params = {
        "status": "FINISHED"
    }

    response = requests.get(url, headers=headers, params=params, timeout=15)
    response.raise_for_status()

    return response.json()


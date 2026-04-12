"""
Load Module

This module handles database operations for loading data.
"""

import os
import logging
import pymysql
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database Configuration
DB_NAME = os.getenv("DB_NAME")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# Get logger
logger = logging.getLogger(__name__)


def get_database_connection():
    """
    Establish connection to MySQL database.

    Returns:
        pymysql.Connection: Database connection object
    """
    try:
        connection = pymysql.connect(
            database=DB_NAME,
            user=DB_USERNAME,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=int(DB_PORT)
        )
        logger.info("Successfully connected to database")
        return connection
    except pymysql.Error as e:
        logger.error(f"Database connection failed: {e}")
        raise


def create_standings_table(connection):
    """
    Create the standings table if it doesn't exist.

    Args:
        connection (pymysql.Connection): Database connection
    """
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS premier_league_standings_tbl (
        position INT PRIMARY KEY,
        team VARCHAR(255),
        games_played INT,
        wins INT,
        draws INT,
        losses INT,
        goals_for INT,
        goals_against INT,
        goal_difference INT,
        points INT
    );
    """

    try:
        with connection.cursor() as cursor:
            cursor.execute(create_table_sql)
            connection.commit()
        logger.info("Standings table created or already exists")
    except pymysql.Error as e:
        logger.error(f"Failed to create table: {e}")
        raise


def load_standings_data(connection, df):
    """
    Load standings data into the database.

    Args:
        connection (pymysql.Connection): Database connection
        df (pd.DataFrame): Standings DataFrame to load
    """
    insert_sql = """
    INSERT INTO premier_league_standings_tbl (
        position, team, games_played, wins, draws, losses, goals_for, goals_against, goal_difference, points
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
    team = VALUES(team),
    games_played = VALUES(games_played),
    wins = VALUES(wins),
    draws = VALUES(draws),
    losses = VALUES(losses),
    goals_for = VALUES(goals_for),
    goals_against = VALUES(goals_against),
    goal_difference = VALUES(goal_difference),
    points = VALUES(points)
    """

    try:
        with connection.cursor() as cursor:
            for idx, row in df.iterrows():
                cursor.execute(insert_sql, (
                    row['P'], row['Team'], row['GP'], row['W'], row['D'],
                    row['L'], row['F'], row['A'], row['GD'], row['Pts']
                ))
            connection.commit()
        logger.info(f"Loaded {len(df)} records into database")
    except pymysql.Error as e:
        logger.error(f"Failed to load data: {e}")
        raise


def create_ranked_view(connection):
    """
    Create a database view for ranked standings.

    Args:
        connection (pymysql.Connection): Database connection
    """
    drop_view_sql = "DROP VIEW IF EXISTS premier_league_standings_vw;"
    create_view_sql = """
    CREATE VIEW premier_league_standings_vw AS
    SELECT
        @rownum := @rownum + 1 AS position,
        team,
        games_played,
        wins,
        draws,
        losses,
        goals_for,
        goals_against,
        goal_difference,
        points
    FROM
        premier_league_standings_tbl,
        (SELECT @rownum := 0) r
    ORDER BY points DESC, goal_difference DESC, goals_for DESC;
    """

    try:
        with connection.cursor() as cursor:
            cursor.execute(drop_view_sql)
            cursor.execute(create_view_sql)
            connection.commit()
        logger.info("Ranked standings view created")
    except pymysql.Error as e:
        logger.error(f"Failed to create view: {e}")
        raise


def get_standings_from_db(connection):
    """
    Retrieve standings data from the database view.

    Args:
        connection (pymysql.Connection): Database connection

    Returns:
        pd.DataFrame: Standings data from database
    """
    import pandas as pd

    query = """
    SELECT
        position, team, games_played, wins, draws, losses,
        goals_for, goals_against, goal_difference, points
    FROM premier_league_standings_vw
    ORDER BY position;
    """

    try:
        df = pd.read_sql(query, connection)
        logger.info(f"Retrieved {len(df)} records from database")
        return df
    except Exception as e:
        logger.error(f"Failed to retrieve data from database: {e}")
        raise</content>
<parameter name="filePath">c:\Users\bchan\Desktop\TUD\project\python_sql_football_data_pipeline\src\load.py
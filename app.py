"""
Streamlit App for Premier League Standings

This app displays Premier League standings from the MySQL database.
"""

import os
import sys
from pathlib import Path

import pandas as pd
from PIL import Image
import plotly.express as px
import streamlit as st
from streamlit.runtime.scriptrunner import get_script_run_ctx
from dotenv import load_dotenv

# Add src directory to path
sys.path.append(str(Path(__file__).resolve().parent / 'src'))

from load import get_database_connection, get_standings_from_db

# Load environment variables
load_dotenv()

# Configuration
IMAGE_FILE_PATH = os.getenv('IMAGE_FILE_PATH', 'assets/premier-league-logo.png')


def main():
    """Main Streamlit app function."""
    st.set_page_config(
        page_title='Premier League Standings 2025/26',
        page_icon='⚽',
        layout='wide'
    )

    connection = None
    final_standings_df = pd.DataFrame()

    try:
        connection = get_database_connection()
        final_standings_df = get_standings_from_db(connection)
    except Exception as e:
        st.error(f'Failed to load standings data: {e}')
        return
    finally:
        if connection is not None:
            try:
                connection.close()
            except Exception:
                pass

    if not final_standings_df.empty:
        final_standings_df.set_index('position', inplace=True)

    try:
        prem_league_logo_image = Image.open(IMAGE_FILE_PATH)
    except FileNotFoundError:
        prem_league_logo_image = None

    if prem_league_logo_image is not None:
        col1, col2 = st.columns([4, 1])
        col2.image(prem_league_logo_image)

    st.title('⚽🏆 Premier League Standings 2025/26 ⚽🏆')
    st.write('')

    st.sidebar.title('Instructions 📖')
    st.sidebar.write(
        'The table showcases the current Premier League standings for the 2025/26 season. Toggle visualizations to gain deeper insights!'
    )

    show_visualization = st.sidebar.radio(
        'Would you like to view the standings as a visualization too?',
        ('No', 'Yes')
    )

    if show_visualization == 'Yes':
        st.table(final_standings_df)
        st.write('')

        fig = px.bar(
            final_standings_df,
            x='team',
            y='points',
            title='Premier League Standings 2025/26',
            labels={
                'points': 'Points',
                'team': 'Team',
                'goals_for': 'Goals Scored',
                'goals_against': 'Goals Conceded',
                'goal_difference': 'Goal Difference'
            },
            color='team',
            height=700,
            hover_data=['goals_for', 'goals_against', 'goal_difference']
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.table(final_standings_df)


def is_running_in_streamlit() -> bool:
    try:
        return get_script_run_ctx() is not None
    except Exception:
        return False


if __name__ == '__main__':
    if not is_running_in_streamlit():
        print('Please run this app with: streamlit run app.py')
        sys.exit(0)
    main()

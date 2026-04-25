"""
Streamlit App for Premier League Dashboard
"""

import os
import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit.runtime.scriptrunner import get_script_run_ctx
from dotenv import load_dotenv

# Add src directory to path
sys.path.append(str(Path(__file__).resolve().parent / 'src'))

from load import get_database_connection, get_standings_from_db

# Load environment variables
load_dotenv()


# ---------- HELPER FUNCTIONS ----------

def format_form(form):
    """Convert form string to colored emojis."""
    if not form:
        return ""
    mapping = {"W": "🟢", "D": "🟡", "L": "🔴"}
    return " ".join(mapping.get(x, x) for x in form)


def highlight_positions(row):
    """Highlight top 4 and bottom 3 teams."""
    try:
        pos = int(row.name)
        if pos <= 4:
            return ['background-color: #d4edda'] * len(row)  # green
        elif pos >= 18:
            return ['background-color: #f8d7da'] * len(row)  # red
    except Exception:
        pass
    return [''] * len(row)


# ---------- MAIN APP ----------

def main():
    st.set_page_config(
        page_title='Premier League Dashboard',
        page_icon='⚽',
        layout='wide'
    )

    st.title('⚽ Premier League Dashboard 2025/26')
    st.markdown("---")

    # ---------- LOAD DATA ----------
    connection = None
    try:
        connection = get_database_connection()
        df = get_standings_from_db(connection)
    except Exception as e:
        st.error(f'Failed to load standings data: {e}')
        return
    finally:
        if connection:
            connection.close()

    if df.empty:
        st.info("⚠️ No standings data available. Run the pipeline first.")
        return

    # ---------- DATA CLEANING ----------
    # Handle form safely
    if 'form' in df.columns:
        df['form'] = df['form'].fillna("").apply(format_form)
    else:
        df['form'] = ""

    # Rename columns for UI
    df.rename(columns={
        'position': 'Pos',
        'team': 'Team',
        'points': 'Pts',
        'goals_for': 'GF',
        'goals_against': 'GA',
        'goal_difference': 'GD',
        'games_played': 'GP',
        'wins': 'W',
        'draws': 'D',
        'losses': 'L',
        'form': 'Form'
    }, inplace=True)

    df.set_index('Pos', inplace=True)

    # Ensure sorted properly
    df = df.sort_index()

    # ---------- SIDEBAR ----------
    st.sidebar.title("⚙️ Controls")

    show_chart = st.sidebar.checkbox("Show Chart", True)
    top_n = st.sidebar.slider("Select Top Teams", 5, 20, 10)

    filtered_df = df.head(top_n)

    # ---------- METRICS ----------
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "🏆 Leader",
        df.iloc[0]['Team'],
        f"{df.iloc[0]['Pts']} pts"
    )

    col2.metric(
        "⚽ Most Goals",
        df.sort_values('GF', ascending=False).iloc[0]['Team']
    )

    col3.metric(
        "🛡️ Best Defense",
        df.sort_values('GA').iloc[0]['Team']
    )

    st.markdown("---")

    # ---------- TABLE ----------
    st.subheader("📊 League Table")

    styled_df = filtered_df.style \
        .apply(highlight_positions, axis=1) \
        .background_gradient(subset=['Pts'], cmap='Greens') \
        .background_gradient(subset=['GD'], cmap='RdYlGn') \
        .set_properties(**{'text-align': 'center'})

    # Use st.write for styling support
    st.write(styled_df)

    # ---------- CHART ----------
    if show_chart:
        st.markdown("---")
        st.subheader("📈 Points Comparison")

        fig = px.bar(
            filtered_df.reset_index(),
            x='Pts',
            y='Team',
            orientation='h',
            color='Pts',
            color_continuous_scale='Viridis',
            hover_data=['GF', 'GA', 'GD', 'Form'],
            height=600
        )

        fig.update_layout(
            yaxis={'categoryorder': 'total ascending'}
        )

        st.plotly_chart(fig, use_container_width=True)


# ---------- STREAMLIT CHECK ----------

def is_running_in_streamlit() -> bool:
    try:
        return get_script_run_ctx() is not None
    except Exception:
        return False


if __name__ == '__main__':
    if not is_running_in_streamlit():
        print('Run this app using: streamlit run app.py')
        sys.exit(0)
    main()
 
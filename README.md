# Football Data Pipeline

A comprehensive ETL (Extract-Transform-Load) pipeline for fetching, processing, and visualizing Premier League football data. Built with Python, MySQL, and Streamlit for production-ready data engineering workflows.

## Overview

This project demonstrates a professional data engineering pipeline that:
- Fetches live Premier League standings from an external API
- Validates data at multiple stages for quality assurance
- Transforms raw data into a structured relational format
- Loads clean data into a MySQL database
- Serves an interactive web dashboard for data exploration

## Architecture

```mermaid
graph TD
    A["🏟️ football-data.org API"] --> B["Extract Module<br/>fetch_football_standings()"]
    B --> C["Validate Module<br/>API Response Check"]
    C --> D["Transform Module<br/>DataFrame Processing"]
    D --> E["Validate Module<br/>Data Quality Check"]
    E --> F["Load Module<br/>Database Operations"]
    F --> G["MySQL Database<br/>premier_league_standings_tbl"]
    
    H["📊 Streamlit App<br/>streamlit run app.py"] --> G
    H --> I["Interactive Visualizations<br/>Charts & Tables"]
    
    J["🐳 Docker Compose"] --> K["MySQL 8.0 Container"]
    J --> L["phpMyAdmin GUI<br/>localhost:8080"]
```

## Project Structure

```
python_sql_football_data_pipeline/
├── src/                           # Core pipeline modules
│   ├── extract.py                # fetch_football_standings() - API data fetching
│   ├── transform.py              # process_standings_data() - DataFrame transformation
│   ├── validate.py               # Data quality validation functions
│   └── load.py                   # Database operations & connection handling
│
├── tests/                         # Unit and integration tests (pytest)
│   ├── test_extract.py
│   ├── test_transform.py
│   ├── test_load.py
│   └── test_validate.py
│
├── assets/                        # Static files
│   └── premier-league-logo.png
│
├── main.py                        # ETL orchestrator (runs pipeline end-to-end)
├── app.py                         # Streamlit web application (dashboard)
├── docker-compose.yml             # MySQL 8.0 + phpMyAdmin containers
├── requirements.txt               # Python package dependencies
├── .env.example                   # Environment variables template
├── .env                           # Actual environment (git-ignored)
├── football_table_standings.log   # Pipeline execution logs
├── README.md                      # This file
└── .git/                          # Version control
```

## Running the Pipeline

### Run Full ETL Pipeline

Executes all stages: Extract → Validate → Transform → Validate → Load

```bash
python main.py
```

**Output:**
- Console logging of each stage
- Database populated with standings
- Log file: `football_table_standings.log`
- Sample output:
  ```
  2026-04-13 02:15:01 - __main__ - INFO - Starting Football Data Pipeline
  2026-04-13 02:15:01 - __main__ - INFO - Step 1: Extracting data
  2026-04-13 02:15:02 - __main__ - INFO - Step 2: Transforming data
  2026-04-13 02:15:02 - __main__ - INFO - Step 3: Loading data to database
  2026-04-13 02:15:03 - __main__ - INFO - Pipeline completed successfully
  ```

### Launch Web Dashboard

**IMPORTANT:** Always use `streamlit run`, NOT `python app.py`

```bash
streamlit run app.py
```

**Access the dashboard:**
- Open browser to: `http://localhost:8501`
- Interactive table showing Premier League standings
- Toggle button to show/hide bar chart visualization
- Responsive layout with Premier League logo

### Database Management

**View database with phpMyAdmin:**
```
URL: http://localhost:8080
Username: root
Password: (from .env MYSQL_PASSWORD)
```

**Query standings directly:**
```bash
mysql -u root -p football_db
SELECT * FROM premier_league_standings_vw ORDER BY position;
```

## Features

### Core Pipeline
- ✅ **Extract**: Fetches live Premier League standings from football-data.org REST API with retry logic
- ✅ **Validate (Pre-Transform)**: Validates API response structure and data completeness
- ✅ **Transform**: Converts raw JSON data into structured Pandas DataFrames with proper schema
- ✅ **Validate (Post-Transform)**: Ensures data quality, type safety, and business rule compliance
- ✅ **Load**: Intelligently inserts or updates records in MySQL using `ON DUPLICATE KEY UPDATE`

### Database Layer
- ✅ **Ranked Views**: Window function-based database views for automatic ranking
- ✅ **Schema Management**: Clean relational schema with proper data types and constraints
- ✅ **Error Handling**: Comprehensive logging for all database operations

### Visualization
- ✅ **Interactive Dashboard**: Real-time standings table with Streamlit
- ✅ **Dynamic Charts**: Plotly-based bar charts showing points distribution
- ✅ **Radio Controls**: Toggle between table and visualization views
- ✅ **Responsive Layout**: Wide layout with logo display and instructions

### Development & Testing
- ✅ **Unit Tests**: pytest-based test suite for core modules
- ✅ **Docker Support**: Docker Compose for isolated MySQL environment
- ✅ **Environment Management**: `.env` configuration for secure credential handling
- ✅ **Logging**: Comprehensive logging to file and console

## Detailed Setup

### 1. Environment Configuration

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
# API Configuration
API_KEY=your_api_key_from_football_data_org
API_HOST=api.football-data.org
LEAGUE_ID=PL
SEASON=2023

# Database Configuration
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=football_db
MYSQL_USERNAME=root
MYSQL_PASSWORD=your_password

# File Paths
IMAGE_FILE_PATH=assets/premier-league-logo.png
```

**Get an API Key:**
1. Visit [football-data.org](https://www.football-data.org/client/home)
2. Sign up for a free account
3. Copy your API key from the dashboard

### 2. Start MySQL Database

**Option A: Using Docker Compose (Recommended)**
```bash
docker-compose up -d
# MySQL: localhost:3306
# phpMyAdmin: localhost:8080 (user: root, password from .env)
```

**Option B: Using Local MySQL**
```bash
mysql -u root -p
CREATE DATABASE football_db;
```

### 3. Install Python Dependencies

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Testing

### Run All Tests

```bash
pytest tests/ -v
```

### Run with Coverage

```bash
pytest --cov=src tests/ --cov-report=html
```

### Available Test Suites

- `test_extract.py` - API fetching and error handling
- `test_transform.py` - Data transformation logic
- `test_validate.py` - Data quality checks
- `test_load.py` - Database operations

### Example Test Run

```bash
$ pytest tests/ -v
tests/test_extract.py::test_fetch_football_standings PASSED      [ 20%]
tests/test_transform.py::test_process_standings_data PASSED      [ 40%]
tests/test_validate.py::test_validate_api_response PASSED        [ 60%]
tests/test_load.py::test_create_standings_table PASSED           [ 80%]
tests/test_load.py::test_load_standings_data PASSED              [100%]
```

## Docker & Containerization

### Start Services

```bash
docker-compose up -d
```

This starts:
- **MySQL 8.0** on `localhost:3306`
- **phpMyAdmin** on `localhost:8080` (user: `root`)
- Persistent data volume: `mysql_data`

### Stop Services

```bash
docker-compose down
```

### View Logs

```bash
# MySQL logs
docker-compose logs -f mysql

# All services
docker-compose logs -f
```

### Database Backup

```bash
docker-compose exec mysql mysqldump -u root -p football_db > backup.sql
```

### Cleanup (WARNING: Deletes Database)

```bash
docker-compose down -v  # Removes volumes too
```

## Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Language** | Python | 3.8+ |
| **Web Framework** | Streamlit | Latest |
| **Data Processing** | Pandas | Latest |
| **Visualization** | Plotly Express | Latest |
| **Database** | MySQL | 8.0 |
| **ORM/Query Library** | PyMySQL | Latest |
| **Testing** | pytest | Latest |
| **API Client** | requests | Latest |
| **Environment** | python-dotenv | Latest |
| **Containerization** | Docker & Compose | Latest |

## Common Commands

```bash
# Activate virtual environment
source .venv/bin/activate

# Run full pipeline
python main.py

# Launch dashboard
streamlit run app.py

# Run tests
pytest tests/ -v

# Database operations
mysql -u root -p football_db

# View logs
tail -f football_table_standings.log

# Docker management
docker-compose up -d
docker-compose down
docker-compose logs -f
```

## Resources & References

- [football-data.org API Documentation](https://www.football-data.org/documentation/api)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [MySQL Window Functions](https://dev.mysql.com/doc/refman/8.0/en/window-functions.html)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [pytest Documentation](https://docs.pytest.org/)

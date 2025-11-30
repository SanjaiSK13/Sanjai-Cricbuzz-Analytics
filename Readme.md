# Cricbuzz LiveStats Dashboard
Author - Sanjai K

# Project Overview

Cricbuzz LiveStats is an interactive web application designed for cricket enthusiasts and data analysts. 
It bridges the gap between live sports data and historical analysis by maintaining a hybrid database of real-time matches fetched via API and engineered historical data for deep analytics.

# Key Features
* **Live Match Dashboard:** View real-time scores, ball-by-ball updates, and detailed scorecards for ongoing matches with an interactive dropdown selector.
* **SQL Analytics Lab:** A dedicated interface to run 25+ Advanced SQL Queries (Partnerships, Year-on-Year trends, Win Margins) on the database.
* **Top Stats & Profiles:** View ICC Player Rankings and search for detailed Player Profiles (Bio, Image, Career Stats).
* **Admin CRUD System:** A back-office tool to manually Create, Read, Update, and Delete player records safely.
* **Hybrid Data Engine:** Seamlessly merges "Mock Historical Data" (for analytics) with "Real Live Data" (from API) in the same MySQL database.

# Project Structure

cricbuzz_livestats/
├── pages/
│   ├── live_matches.py    # Real-time Scorecard Dashboard
│   ├── top_stats.py       # ICC Rankings & Player Search
│   ├── sql_queries.py     # 25+ SQL Questions Interface
│   └── crud_perations.py  # Admin Management Panel
├── utils/
│   ├── api_handler.py     # Cricbuzz API logic (Search, Scorecard, Rankings)
│   ├── db_connection.py   # MySQL Connection & Engine logic
│   └── queries.py         # Dictionary of 25 SQL Queries
├── .env                        # API Keys & Database Credentials (Secrets)
├── main.py                     # Home Page & Navigation Hub
├── mock_data_generator.py      # Script to seed database with 150+ historical matches
├── real_data_loader.py         # Script to fetch & append live data from API
├── requirements.txt            # Python Dependencies
└── README.md                   # Project Documentation

## Setup and Installation

1. Clone and install dependencies.
   # Install required Python libraries
      pip install -r requirements.txt

2. Initializing the Database
  This project uses a Hybrid Data Strategy. Run these scripts in order to build the database schema and populate it with data.

   -> Run this loader to fetch the latest matches from Cricbuzz API and append them to your database.
       python real_data.py
   -> Run this generator to create additional records which may be used for analytics.
       python mock_data_generator.py
   -> API credentials are given in the .env file
   
3. Launching the web application
    streamlit run main.py

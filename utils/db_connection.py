import os
import pandas as pd
from sqlalchemy import create_engine, text
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME", "cricbuzz_livestats")
DB_PORT = os.getenv("DB_PORT", "3306")

def create_database_if_not_exists():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        conn.close()
    except Exception as e:
        print(f"❌ Initial Setup Error: {e}")

def get_engine():
    create_database_if_not_exists()
    connection_str = f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(connection_str)

def init_tables():
    try:
        engine = get_engine()
        with engine.connect() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS matches (
                    match_id INT PRIMARY KEY,
                    series_name VARCHAR(100),
                    match_desc VARCHAR(255),
                    venue_name VARCHAR(100),
                    city VARCHAR(100),
                    country VARCHAR(100),
                    match_date VARCHAR(50),
                    team1 VARCHAR(100),
                    team2 VARCHAR(100),
                    winner VARCHAR(100)
                );
            """))

            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS players (
                    player_id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) UNIQUE,
                    country VARCHAR(50),
                    role VARCHAR(50),
                    batting_style VARCHAR(50),
                    bowling_style VARCHAR(50)
                );
            """))

            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS player_stats (
                    player_id INT AUTO_INCREMENT PRIMARY KEY,
                    player_name VARCHAR(100) UNIQUE,
                    matches INT DEFAULT 0,
                    runs INT DEFAULT 0,
                    average DECIMAL(10, 2) DEFAULT 0.00
                );
            """))
            
            conn.commit()
    except Exception as e:
        print(f"❌ Table Init Error: {e}")

def run_query(query_str, params=None):
    try:
        engine = get_engine()
        with engine.connect() as conn:
            if params:
                return pd.read_sql(text(query_str), conn, params=params)
            return pd.read_sql(text(query_str), conn)
    except Exception as e:
        return f"Error: {e}"

def execute_crud(query_str, params=None):
    try:
        engine = get_engine()
        with engine.connect() as conn:
            conn.execute(text(query_str), params or {})
            conn.commit()
            return "Success"
    except Exception as e:
        return f"Error: {e}"


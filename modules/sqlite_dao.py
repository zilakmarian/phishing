"""Helper module for dealing with SQLite database operations."""
import sqlite3
from datetime import datetime
from typing import Optional
from urllib.parse import urlparse

import modules.downloader as downloader


class SQLiteDAO(object):
    """Database Access Object for handling data stored in underlying database."""
    _database_path = None

    def __init__(self, database_path: str):
        self._database_path = database_path

    def initiate_database(self, url: str):
        """Create table and store data downloaded from provided url."""
        self._create_table()
        data = downloader.download(url)
        for d in data:
            d["domain"] = self._parse_domain(d["url"])

        self._load_data(data)

    def search_by_date(self, date_from: datetime, date_to: Optional[datetime] = None):
        """Search for urls in database based on datetime range."""
        with sqlite3.connect(self._database_path) as connection:
            connection.row_factory = sqlite3.Row
            args = [date_from]
            query = """SELECT full_url as url, domain as domain
            FROM report WHERE datetime(submission_time) >= datetime(?)"""
            if date_to:
                query += " AND datetime(submission_time) <= datetime(?)"
                args.append(date_to)

            return connection.execute(query, args).fetchall()

    def search_by_domain(self, domain: str):
        """Search for phish_url based on domain."""
        with sqlite3.connect(self._database_path) as connection:
            connection.row_factory = sqlite3.Row
            query = "SELECT phish_url FROM report WHERE domain = ?"
            return connection.execute(query, (domain, )).fetchall()

    def _create_table(self):
        """Create table for storing phishtank reports."""
        with sqlite3.connect(self._database_path) as connection:
            connection.execute("""CREATE TABLE IF NOT EXISTS report(
                           phish_id INTEGER NOT NULL PRIMARY KEY,
                           phish_url TEXT,
                           full_url TEXT,
                           domain TEXT,
                           submission_time TEXT
                           )""")

    def _load_data(self, data: list[dict]):
        """Store data in database."""
        with sqlite3.connect(self._database_path) as connection:
            upsert_query = """INSERT INTO report
            VALUES (:phish_id, :phish_detail_url, :url, :domain, :submission_time)
            ON CONFLICT DO UPDATE SET
            phish_url=excluded.phish_url,
            full_url=excluded.full_url,
            domain=excluded.domain,
            submission_time=excluded.submission_time
            """
            connection.executemany(upsert_query, data)

    @staticmethod
    def _parse_domain(url: str):
        return urlparse(url).netloc


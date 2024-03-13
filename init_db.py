"""Download and store phishtank data in database."""
from modules.sqlite_dao import SQLiteDAO

if __name__ == "__main__":
    PHISHTANK_URL = "https://data.phishtank.com/data/online-valid.json"
    DATABASE_PATH = "/data/report.db"

    dao = SQLiteDAO(DATABASE_PATH)
    dao.initiate_database(url=PHISHTANK_URL)

"""Module for starting up the webserver application."""
import re
import os
from collections import Counter
from datetime import datetime
from typing import Optional

from fastapi import FastAPI

from modules.sqlite_dao import SQLiteDAO


def create_app():
    """Create WSGI application."""
    DATABASE_PATH = "/data/report.db"
    if not os.path.exists(DATABASE_PATH):
        raise Exception("Phishtank report database does not exist.")

    app = FastAPI()
    dao = SQLiteDAO(DATABASE_PATH)

    @app.get("/download_report")
    def download_report(date_from: datetime, date_to: Optional[datetime] = None):
        """Return JSON with list of urls, number or urls and TLDs in specified range."""
        rows = dao.search_by_date(date_from, date_to)
        urls = [r["url"] for r in rows]
        tld_pattern = r"\.[^.]+$"
        tlds = []
        for row in rows:
            match = re.search(tld_pattern, row["domain"])
            domain = match[0] if match else None
            tlds.append(domain)

        tlds = [{"domain": d, "count": c} for d, c in Counter(tlds).most_common()]
        return {"urls": urls, "number_of_results": len(urls), "top_level_domains": tlds}

    @app.get("/search_domain")
    def search_domain(domain: str):
        """Return JSON with a list of phishtank urls for specified domain."""
        results = dao.search_by_domain(domain)
        return {"phistank_urls": [r["phish_url"] for r in results]}

    return app


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:create_app", port=5000)

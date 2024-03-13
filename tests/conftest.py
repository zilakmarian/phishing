import pytest
from modules.sqlite_dao import SQLiteDAO


@pytest.fixture
def sqlite_dao(tmp_path):
    return SQLiteDAO(str(tmp_path / "report.db"))

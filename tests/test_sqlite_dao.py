from datetime import datetime


data = [{"phish_id": 1,
         "url": "https://first.fake.url/some/arguments?and=params",
         "phish_detail_url": "http://fake.details.url/1",
         "submission_time": "2024-03-10T10:00:00+00:00",
         "domain": "first.fake.url"
         },
        {"phish_id": 2,
         "url": "https://second.fake.url/other/arguments?diff=params2",
         "phish_detail_url": "http://fake.details.url/2",
         "submission_time": "2024-03-10T12:00:00+00:00",
         "domain": "second.fake.url"
         },
        {"phish_id": 3,
         "url": "https://second.fake.url/differen/path/same/domain",
         "phish_detail_url": "http://fake.details.url/3",
         "submission_time": "2024-03-10T20:00:00+00:00",
         "domain": "second.fake.url"
         }
        ]


def test_parse_domain(sqlite_dao):
    """Test parsing domain from url."""
    result = sqlite_dao._parse_domain("https://second.fake.url/some/path?param=1")
    assert result == "second.fake.url"


def test_search_by_date(sqlite_dao):
    """Test searching by date range."""
    sqlite_dao._create_table()
    sqlite_dao._load_data(data)
    # Search by date_from only
    date_from = datetime.fromisoformat("2024-03-10T12:00:00+00:00")
    result = sqlite_dao.search_by_date(date_from)
    assert len(result) == 2
    # Search by both date_from and date_to
    date_to = datetime.fromisoformat("2024-03-10T19:00:00+00:00")
    result = sqlite_dao.search_by_date(date_from, date_to)
    assert len(result) == 1
    assert result[0]["url"] == "https://second.fake.url/other/arguments?diff=params2"
    assert result[0]["domain"] == "second.fake.url"
    # Searching for non-existent date
    date_from = datetime.fromisoformat("2024-03-20T00:00:00+00:00")
    result = sqlite_dao.search_by_date(date_from)
    assert len(result) == 0


def test_search_by_domain(sqlite_dao):
    """Test searching by domain name."""
    sqlite_dao._create_table()
    sqlite_dao._load_data(data)
    # Search for existing domain
    result = sqlite_dao.search_by_domain("second.fake.url")
    assert len(result) == 2
    # Search for non-existent domain
    result = sqlite_dao.search_by_domain("no.such.domain")
    assert len(result) == 0
    # Accept only exact searches of url, no partials are allowed
    result = sqlite_dao.search_by_domain("fake.url")
    assert len(result) == 0

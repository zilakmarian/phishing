# Phishing report API
Simple HTTP API for downloading and searching in phishtank.org database.

## Installation notes
Requires: 
- docker
- docker compose
- internet access (for downloading python docker image)


## Usage
For easy startup of webserver, use `docker compose up`.
If you prefer the hard way, create a volume and map it to container path `/data/`, load it with data using by running `init_db.py` script and then start the app container with volume mounted.   

Once the application boots up, it will accept GET requests with following paths:
- `GET /download_report`: accepts URL parameters `date_from` and `date_to` as datetime string. E.g.:
```
curl -X 'GET' \
  'http://127.0.0.1:5000/download_report?date_from=2024-03-05T10%3A00%3A00%2B00%3A00&date_to=2024-03-06T10%3A00%3A00%2B00%3A00' \
  -H 'accept: application/json'
```

- `GET /search_domain`: accepts URL parameter `domain` for searching by full domain name (everything between schema and path). E.g.:
```
curl -X 'GET' \
  'http://127.0.0.1:5000/search_domain?domain=docs.google.com' \
  -H 'accept: application/json'
```

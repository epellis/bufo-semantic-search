## Setup

### Setup webserver

```sh
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Download Assets

```sh
cd ~
git clone https://github.com/knobiknows/all-the-bufo.git
```

### Run Server

```sh
cd bufo-semantic-search

# example:
ALL_THE_BUFO_DIR="/Users/e/all-the-bufo/all-the-bufo" gunicorn "app:app"
```

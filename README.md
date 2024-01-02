## Setup

### Setup webserver

```sh
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -f https://download.pytorch.org/whl/torch_stable.html
```

### Download Assets

```sh
cd ~
git clone https://github.com/knobiknows/all-the-bufo.git
```

###

```
sudo vim /etc/supervisor/conf.d/bufo.conf
```

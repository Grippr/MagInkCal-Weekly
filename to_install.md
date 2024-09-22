Hardware
- Raspbery Pi Zero 2 WH
- python 3.11.2
- Raspberry Pi Os Lite (64-Bit)

Installation
- `sudo apt upgrade`
- `sudo apt update`
- `sudo apt-get install git`
- `sudo apt-get install netcat-openbsd`
- `git clone https://github.com/Grippr/Rasp-A-Glance.git`
- `python -m venv raspaglance-venv`
- `. raspaglance-venv/bin/activate`

- Required python packages
    - `pytest`
    - `json5`
    - `pytz`
    - `google-api-python-client`
    - `google-auth-httplib2`
    - `google-auth-oauthlib`
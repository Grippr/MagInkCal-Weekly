Hardware
- Raspbery Pi Zero 2 WH
- python 3.11.2
- Raspberry Pi Os Lite (64-Bit)

Installation
- `sudo apt upgrade`
- `sudo apt update`
- `sudo apt-get install git`
- `sudo apt-get install netcat-openbsd`
- `sudo apt-get install python3-setuptools`
- Install lg Library:
```
wget https://github.com/joan2937/lg/archive/master.zip
unzip master.zip
cd lg-master
make
sudo make install
```


- `git clone https://github.com/Grippr/MagInkCalPy.git`
- `python -m venv maginkcal-venv`
- `. maginkcal-venv/bin/activate`

- Required python packages
    - `pytest`
    - `json5`
    - `pytz`
    - `google-api-python-client`
    - `google-auth-httplib2`
    - `google-auth-oauthlib`
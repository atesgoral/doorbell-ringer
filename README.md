[![Build Status](https://travis-ci.org/atesgoral/doorbell-ringer.svg?branch=master)](https://travis-ci.org/atesgoral/doorbell-ringer)

# doorbell-ringer
Rings a doorbell

# Setup

## Prepare Onion Omega

### Mount USB Drive

### Install Python and Git

```sh
opkg update
opkg install python-light python-pip git git-http
```

## Install Service

```sh
mkdir /opt
cd opt
git clone https://github.com/atesgoral/doorbell-ringer.git
```

## Setup Python Environment for Onion Omega or Local Development

```sh
pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run Service

```sh
python stream.py
```

## Run Tests

```sh
python -m unittest discover -s test
```

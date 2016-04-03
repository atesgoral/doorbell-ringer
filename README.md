[![Build Status](https://travis-ci.org/atesgoral/doorbell-ringer.svg?branch=master)](https://travis-ci.org/atesgoral/doorbell-ringer)

# doorbell-ringer
This is a Python service that runs on an [Onion Omega](https://onion.io/omega). As the [@DoorbellRinger](https://twitter.com/DoorbellRinger) Twitter account, it watches the user stream and rings a doorbell when [@DoorbellNudger](https://twitter.com/DoorbellNudger) tweets something with the #ringit hashtag.

## Setup

### Prepare Onion Omega

#### Mount USB Drive

Follow the pivot-overlay section:

https://wiki.onion.io/Tutorials/Using-USB-Storage-as-Rootfs

#### Install Python and Git

```sh
opkg update
opkg install python-light python-pip git git-http
```

### Python Environment for Onion Omega or Local Development

```sh
pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Additional Setup for Local Development

To stub out the `expled` and `ubus` commands available on Omega's OpenWRT, you can copy the contents of the stubs directory to your bin folder or add the stubs folder to your PATH.

### Additional Setup for Onion Omega

Create a symbolic link to the init.d script and enable the service to start on boot:

```sh
ln -s /opt/doorbell-ringer/init.d.sh /etc/init.d/doorbell-ringer
/etc/init.d/doorbell-ringer enable
reboot
```

### Run Service

```sh
python stream.py
```

### Run Tests

```sh
python -m unittest discover -s test
```

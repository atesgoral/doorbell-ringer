[![Build Status](https://travis-ci.org/atesgoral/doorbell-ringer.svg?branch=master)](https://travis-ci.org/atesgoral/doorbell-ringer)

# doorbell-ringer
This is a Python service that runs on an [Onion Omega](https://onion.io/omega). As the [@DoorbellRinger](https://twitter.com/DoorbellRinger) Twitter account, it watches the user stream and rings a doorbell when [@DoorbellNudger](https://twitter.com/DoorbellNudger) tweets something with the `#ringit` hashtag. It also auto-updates with the `#update` hashtag.

## Onion Omega Setup

### Mount USB Drive

Follow the pivot-overlay section:

https://wiki.onion.io/Tutorials/Using-USB-Storage-as-Rootfs

tl;dr:

```sh
opkg update
opkg install e2fsprogs
mkfs.ext4 /dev/sda1
mkdir /mnt/sda1
mount /dev/sda1 /mnt/sda1/
mount /dev/sda1 /mnt ; tar -C /overlay -cvf - . | tar -C /mnt -xf - ; umount /mnt
block detect > /etc/config/fstab
```
Edit /etc/config/fstab:

```
option target '/overlay'
option enabled '1'
```

Then reboot your Omega.

### Install Python and Git

```sh
opkg update
opkg install python-light python-pip git git-http
```

### Get the Service

Clone this repository (via HTTPS) into the /opt directory:

```sh
mkdir /opt
cd /opt
git clone https://github.com/atesgoral/doorbell-ringer.git
```

### Install Python Packages

```sh
cd /opt/doorbell-ringer
pip install -r requirements.txt
```

### Configure the Service

Make a copy of config.yml.example as config.yml and fill in your Twitter Application's access settings:

```yml
twitter:
  consumerKey: ...
  consumerSecret: ...
  accessTokenKey: ...
  accessTokenSecret: ...
```

### Set up the Service to Run on Boot

Create a symbolic link to the init.d script and enable the service:

```sh
ln -s /opt/doorbell-ringer/init.d.sh /etc/init.d/doorbell-ringer
/etc/init.d/doorbell-ringer enable
reboot
```

### Start the Service

After the service is set up to run on boot, just reboot the Omega. Or manually start the service:

```sh
/etc/init.d/doorbell-ringer start
```

### Manually Running the Service

```sh
python stream.py
```

## Local Development

To stub out the `expled` and `ubus` commands available on Omega's OpenWRT, you can copy the contents of the stubs directory to your bin folder or add the stubs folder to your PATH.

### Running the Tests

```sh
python -m unittest discover -s test
```

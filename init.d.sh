#!/bin/sh /etc/rc.common

START=10
STOP=15

EXTRA_COMMANDS="update"
EXTRA_HELP="        update  Update to latest"

update() {
  echo "Updating Doorbell Ringer"
  cd /opt/doorbell-ringer
  git fetch
  git reset --hard origin/master
}

start() {
  echo "Starting Doorbell Ringer"
  python /opt/doorbell-ringer/stream.py &
}

stop() {
  echo "Stopping Doorbell Ringer"
  killall python
}


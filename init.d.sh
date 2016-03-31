#!/bin/sh /etc/rc.common

START=10
STOP=15
 
start() {        
    echo "Starting Doorbell Ringer"
    python /opt/doorbell-ringer/stream.py &
}                 
 
stop() {          
    echo "Stopping Doorbell Ringer"
    killall python
}

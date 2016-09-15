#!/bin/sh



DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

SCRIPT=$DIR'/../voyager/houston.py'
RUNAS=root

PIDFILE='/var/run/houston.pid'
LOGFILE='/var/log/houston.log'

start() {
  sleep 3
  if [ -f /var/run/$PIDNAME ] && kill -0 $(cat /var/run/$PIDNAME); then
    echo 'Service already running' >&2
    return 1
  fi
  echo 'Starting service houston' >&2
  local CMD="$SCRIPT &> \"$LOGFILE\" & echo \$!"
  su -c "$CMD" $RUNAS > "$PIDFILE"
  echo 'Service started  houston' >&2
}

stop() {
  if [ ! -f "$PIDFILE" ] || ! kill -0 $(cat "$PIDFILE"); then
    echo 'Service not running houston' >&2
    return 1
  fi
  echo 'Stopping service houston' >&2
  kill -15 $(cat "$PIDFILE") && rm -f "$PIDFILE"
  echo 'Service stopped houston' >&2
}

case "$1" in
  start)
    start
    ;;
  stop)
    stop
    ;;
  restart)
    stop
    start
    ;;
  *)
    echo "Usage: $0 {start|stop|restart}"
esac
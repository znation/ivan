#!/bin/bash

set -eu

strFilter="$1"

# both current and old log files
# only lines with datetime
# sort by datetime and dbgmsgId
while true;do
  cat ~/.vale.dbgmsg.log* ~/.vale/.vale.dbgmsg.log* \
    |egrep -a "..../../..-..:..:.." \
    |sort -t '(' -k 1.1,1.19 -k 2.1n \
    |egrep -ai "$1" \
    &&:

  ls -l ~/.vale.dbgmsg.log* ~/.vale/.vale.dbgmsg.log*&&:
  echo "================== `date` ================="
  sleep 1
done

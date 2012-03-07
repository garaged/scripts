#!/bin/bash
RANGE=100
while ( true )
do
  imapfilter -c imapfilter.lua
  date
  num=$RANDOM
  let "num %= $RANGE"
  if [ $num -ge 90 ]; then offlineimap; notmuch new; fi
  sleep 240
done

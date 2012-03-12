#!/bin/bash
RANGE=100
while ( true )
do
  imapfilter -c imapfilter.lua
  date
  num=$RANDOM
  let "num %= $RANGE"
  if [ $num -ge 95 ]; then offlineimap -c imapfilter.lua; notmuch new; fi
  sleep 240
done

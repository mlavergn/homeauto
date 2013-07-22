#!/bin/bash

echo "Finding iCamSource pid"
PID=`ps A | grep -i iCamSource | grep -v grep | cut -f 2 -d ' '`
echo "Killing $PID"
kill $PID
echo "Respawning iCamSource"
open -a iCamSource
echo "Done"


#!/bin/bash

CSUP=`ps A | grep iCamSource -c`
if [ $CSUP != 2 ]; then
  open -a /Applications/iCamSource.app
fi

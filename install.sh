#!/bin/bash

FNAME=com.ixtli.rabbitmon.plist
TARGET_DIR=~/Library/LaunchAgents/
TARGET=$TARGET_DIR$FNAME

cp ./$FNAME $TARGET 
chown root $TARGET && chmod 644 $TARGET && launchctl load $TARGET 

#!/bin/bash
export SDIR=/home/pi/src/broadband-connection-test/py/
python3 -m venv $SDIR/.venv
python3 $SDIR/connectionTest.py
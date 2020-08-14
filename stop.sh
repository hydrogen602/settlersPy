#!/bin/bash

PID=$(cat runPID)

kill $PID
echo 'Killing program'
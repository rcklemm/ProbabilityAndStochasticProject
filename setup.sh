#!/bin/bash

# need performance counter API
sudo apt install libpapi-dev

# need user-mode access to performance trackers
sudo sh -c 'echo -1 > /proc/sys/kernel/perf_event_paranoid'


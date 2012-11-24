#!/bin/bash
while true; do
    date
    bin/python -m randblog.admin rss update
    date
    sleep 900
done


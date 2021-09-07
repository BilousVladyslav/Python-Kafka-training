#!/bin/sh

python main.py worker -l info

exec "$@"

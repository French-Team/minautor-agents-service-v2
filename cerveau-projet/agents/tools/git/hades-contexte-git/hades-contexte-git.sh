#!/usr/bin/env bash
# hades-contexte-git.sh - wrapper de parite (delegue au .py)
exec python3 "$(dirname "$0")/hades-contexte-git.py" "$@"

#!/usr/bin/env bash
set -euo pipefail

usage() {
    echo "Usage: ${0##*/} [-n COUNT] [-m MESSAGE]"
    echo "  -n COUNT    Iterate COUNT times (default: infinite)"
    echo "  -m MESSAGE  Print MESSAGE after the iteration number"
    exit 1
}

COUNT=""
MESSAGE=""
while getopts ":n:m:h" opt; do
    case $opt in
        n) COUNT="$OPTARG" ;;
        m) MESSAGE="$OPTARG" ;;
        h) usage ;;
        \?) echo "Invalid option: -$OPTARG" >&2; usage ;;
        :)  echo "Option -$OPTARG requires an argument" >&2; usage ;;
    esac
done
shift $((OPTIND - 1))

if [[ -n "$COUNT" ]]; then
    if ! [[ "$COUNT" =~ ^[0-9]+$ ]]; then
        echo "Error: -n requires a non-negative integer" >&2
        exit 1
    fi
    for ((i = 0; i < COUNT; i++)); do
        echo "Loop Echo $((i + 1))/${COUNT}${MESSAGE:+: $MESSAGE}"
        sleep 2
    done
else
    i=1
    while true; do
        echo "Loop Echo ${i}${MESSAGE:+: $MESSAGE}"
        sleep 2
        ((i++))
    done
fi

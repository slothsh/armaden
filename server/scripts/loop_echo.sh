#!/usr/bin/env bash
set -euo pipefail

usage() {
    echo "Usage: ${0##*/} [-n COUNT]"
    echo "  -n COUNT  Iterate COUNT times (default: infinite)"
    exit 1
}

COUNT=""
while getopts ":n:h" opt; do
    case $opt in
        n) COUNT="$OPTARG" ;;
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
        echo "Message $((i + 1))/${COUNT}: Foo bar baz"
        sleep 2
    done
else
    i=1
    while true; do
        echo "Message ${i}: Foo bar baz"
        sleep 2
        ((i++))
    done
fi

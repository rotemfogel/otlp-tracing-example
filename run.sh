#!/bin/sh
# Start the stack, then open Jaeger in Chrome once its UI responds.
docker compose up -d --build "$@" || exit 1
until curl -sf -o /dev/null http://localhost:16686; do sleep 1; done
open -a "Google Chrome" http://localhost:16686  # macOS; use xdg-open/google-chrome on Linux
while true; do curl -XGET http://localhost:5000/orchestrate ; sleep 5; done
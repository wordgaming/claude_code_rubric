#!/bin/bash
NAMESPACE="${1:-codebase_b845_app}"
docker build -t "$NAMESPACE" .
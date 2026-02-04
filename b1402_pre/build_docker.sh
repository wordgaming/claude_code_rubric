#!/bin/bash
NAMESPACE="${1:-codebase_b1402_app}"
docker build -t "$NAMESPACE" .
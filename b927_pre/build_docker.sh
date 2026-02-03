#!/bin/bash
NAMESPACE="${1:-codebase_b927_app}"
docker build -t "$NAMESPACE" .
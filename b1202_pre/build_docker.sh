#!/bin/bash
NAMESPACE="${1:-codebase_b1202_app}"
docker build -t "$NAMESPACE" .
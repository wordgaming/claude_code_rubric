#!/bin/bash
NAMESPACE="${1:-codebase_b845_app}"
shift 2>/dev/null || true

DETACH=""
RM_FLAG="--rm"

for arg in "$@"; do
    case "$arg" in
        -core.py|--detach) DETACH="-d" ;;
        -k|--keep) RM_FLAG="" ;;
    esac
done

docker run $DETACH -it $RM_FLAG "$NAMESPACE"
#!/bin/bash
python3 -m pip install -r requirements-dev.txt
bash scripts/CD.sh -a
bash scripts/CI.sh

aws athena start-query-execution --query-string "$(cat scripts/evaluation_store.sql | tr '\n' ' ')"

#!/bin/bash
bash scripts/CD.sh -a
bash scripts/CI.sh

aws athena start-query-execution --query-string "$(cat evaluation_store.sql | tr '\n' ' ')"

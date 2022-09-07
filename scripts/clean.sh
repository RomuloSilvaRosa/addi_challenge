#!/bin/bash

aws athena start-query-execution --query-string "DROP TABLE IF EXISTS addi_challenge_v1" | true
aws s3 rm s3://addi-challenge-evaluation-store --recursive | true

get_images(){
    aws ecr list-images --repository-name $1 --query 'imageIds[*]' --output json
}
delete_images(){
    echo $1 $2
    aws ecr batch-delete-image --repository-name $1 --image-ids "$2" > /dev/null 2>&1 || true
}
delete_all_images() {
    IMAGES_TO_DELETE=$(get_images $1)
    delete_images $1 $IMAGES_TO_DELETE
}
delete_all_images model/lambda
delete_all_images orchestrator/lambda
bash scripts/CI.sh -d



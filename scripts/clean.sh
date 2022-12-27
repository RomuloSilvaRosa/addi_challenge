#!/bin/bash

clean_athena() {
    echo "Cleaning Athena"
    aws athena start-query-execution --query-string "DROP TABLE IF EXISTS evaluation_store_table.showcase_mlops_feature_model_evaluation_store_v1" >/dev/null 2>&1 | true
}
clean_s3() {
    echo "Cleaning s3"
    aws s3 rm s3://company-showcase-evaluation-store --recursive
}
get_images() {
    aws ecr list-images --repository-name $1 --query 'imageIds[*]' --output json
}
delete_images() {
    echo "Deleting images from ecr repo $1: $2"
    aws ecr batch-delete-image --repository-name $1 --image-ids "$2" >/dev/null 2>&1 || true
}
delete_all_images() {
    IMAGES_TO_DELETE=$(get_images "$1")
    delete_images $1 "${IMAGES_TO_DELETE}"
}

clean_athena
clean_s3
delete_all_images model/lambda
delete_all_images orchestrator/lambda
bash scripts/CD.sh -d

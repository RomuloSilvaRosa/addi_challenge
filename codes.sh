#!/bin/bash

deploy_code() {
    echo "Deploying $1"
    cd $1
    make docker_build docker_push update_function
    cd -
}

deploying() {
    echo "Deployint Applications"
    cd codes
    for x in $(ls); do
        deploy_code $x
    done
    cd -
}

deploying
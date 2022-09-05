#!/bin/bash

apply_terraform() {
    echo "Applying $1"
    cd $1
    terraform init && terraform apply -auto-approve
    cd -
}

apply_infraestructure() {
    echo "Applying Infraestructure"
    cd infraestructure
    for x in $(ls); do
        apply_terraform $x
    done
    cd -
}

destroy_terraform() {
    echo "Destroying $1"
    cd $1
    terraform init && terraform destroy -auto-approve
    cd -
}

destroy_infraestructure() {
    echo "Destroying Infraestructure"
    cd infraestructure
    for x in $(ls); do
        destroy_terraform $x
    done
    cd -
}

usage() {
    echo "$0 usage:" && grep " .)\ #" $0
    exit 0
}
[ $# -eq 0 ] && usage

DESTROY=0
while getopts "da" arg; do
    case $arg in
    d) # Destroy
        DESTROY=1
        ;;
    a) # Apply.
        DESTROY=0
        ;;
    h) # Display help.
        usage
        exit 0
        ;;
    esac
done
if [[ $DESTROY == 1 ]]; then
    destroy_infraestructure
else
    apply_infraestructure
fi

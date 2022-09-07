#!/bin/bash

apply_infraestructure() {
    echo "Applying Infraestructure"
    cd infraestructure
    make apply
    cd -
}

destroy_infraestructure() {
    echo "Destroying Infraestructure"
    cd infraestructure
    make destroy
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

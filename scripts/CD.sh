#!/bin/bash

apply_infrastructure() {
    echo "Applying Infrastructure"
    cd infrastructure
    make apply
    cd -
}

destroy_infrastructure() {
    echo "Destroying Infrastructure"
    cd infrastructure
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
    destroy_infrastructure
else
    apply_infrastructure
fi

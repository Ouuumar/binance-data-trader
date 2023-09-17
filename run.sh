#!/bin/bash

usage() { 
    echo "Usage: -f : Run project for first time or changes made
    -a : Run project if already ran once and no changes
    -d : Down the project" 
}

export_env() {
    set -a
    source .env
    set +a
}

docker_up_and_build() {
    docker-compose -f docker-compose.yaml up -d --build
}

docker_up() {
    docker-compose -f docker-compose.yaml up -d
}

docker_down() {
    docker-compose -f docker-compose.yaml down
}


export_env

while getopts ":fadu" option; do
    case $option in
    f) # Run project for first time or changes made
        docker_up_and_build
        exit
        ;;
    a)  # Run project if already ran once and no changes
        docker_up
        exit
        ;;
    d) # Down the project
        docker_down
        exit
        ;;
    u) # Documentation help
        usage
        exit
        ;;
    esac
done
#!/bin/bash

usage() { 
    echo "Usage: -b : Run project for first time or changes made
    -i : If need to init airflow
    -u : Run project if already ran once and no changes
    -d : Down the project" 
}

export_env() {
    set -a
    source .env
    set +a
}

init_airflow(){
    docker compose up airflow-init
}

copy_func() {
    cp ./func/functions.py ./api/
    mkdir ./airflow/func/ 
    cp ./func/functions.py ./airflow/func/
}

delete_copy_func() {
    rm -f ./api/functions.py 
}   

docker_up_and_build() {
    docker-compose up -d --build
}

docker_up() {
    docker-compose up -d
}

docker_down() {
    docker-compose down --volumes --remove-orphans
}

export_env

while getopts ":biudh" option; do
    case $option in
    b) # Run project for first time or changes made
        copy_func
        docker_up_and_build
        delete_copy_func
        exit
        ;;
    i) # Init airflow
        init_airflow
        exit
        ;;
    u)  # Run project if already ran once and no changes
        docker_up
        exit
        ;;
    d) # Down the project
        docker_down
        exit
        ;;
    h) # Documentation help
        usage
        exit
        ;;
    esac
done
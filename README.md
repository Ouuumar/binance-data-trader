# Crypto Data Pipelines Application :chart_with_upwards_trend: !

This project allows you to deploy a microservice architecture to live interract with Klines crypto and visualize it through a built FastAPI and Dash application (real-time dashboard)

You can easily query the API to get different informations on the data which is daily updated.

# Start the project :heavy_check_mark: !

You need [Docker](https://www.docker.com/products/docker-desktop/M) installed

Configure your own **`.env`** file with respective credentials for [MySQL](https://www.mysql.com/)

Go to the root folder **`binance-data-trader`** of the project

- If first time you run the project, enter in your **CLI** :
 
```bash 
   ./run.sh -b
```
- If containers are stopped and no changes were done (means images are already built)

```bash 
   ./run.sh -u
```

# Use the application :dart: ! 

After launching the project, go to [localhost:8000](localhost:8080)

You can see the documentation here [localhost:8000/docs](localhost:8080/docs) and see what you can do

To view live Klines go to [localhost:8050](localhost:8050)

# Stop the project :x: !

```bash 
   ./run.sh -d
```

# Architecture :computer:

# Data model :page_with_curl:

# Author :boy:

- [Omar ALLOUACHE](https://www.linkedin.com/in/omar-allouache/)

# Contributing :clap:

I will be glad if you want to add more features or best practices :heart_eyes: ! Do not hesitate to contact me, open issues, PR etc. :blush: 

*The project is not totally done and need some refactoring to be user-coder friendly.*
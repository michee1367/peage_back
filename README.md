# Doc

## Require

- Docker 
- Docker-compose

## create config file
```bash
    cp ./src/config.example.py ./src/config.py
```

## create .env file
```bash
    cp .env.example .env
```
## Demarrer 
```bash
    docker compose up --build -d

```
## Attente
- Attendre au moins 15 secondes;



## Load Data
```bash

    scp path/to/local/data.zip root@sever_ip:/path/to/server
    unzip path/to/local/data.zip -d /path/to/project/src
    source loaddata.sh

```
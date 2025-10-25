# Doc

## Require

- linux os (Ubuntu )
- python 3.8.10 in your machine 
- pip 20.0.2 from /home/nkusu/projects/flask/mvc/venv/lib/python3.8/site-packages/pip (python 3.8)


## install the package

-   sudo apt update
-   sudo apt-get install libpq-dev
-   sudo apt-get install python-dev-is-python3
-   sudo apt-get install python3-wheel
-   pip3 install wheel
-   sudo apt install postgresql postgresql-contrib
-   sudo apt install postgis postgresql-14-postgis-3
-   sudo -i -u postgres
-   psql

## Create database

-   CREATE DATABASE mvc_test;
-   \l
-   \c mvc_test;
-   CREATE EXTENSION postgis;
-   CREATE EXTENSION postgis_topology;

## Init command

- Create vitual environement

```bash

    python3 -m venv venv

```


- Activate the vitual environement

```bash

    source venv/bin/activate

```

- create postgis extension
```
    open pgAdmin
    select (click) your database
    click "SQL" icon on the bar
    run "CREATE EXTENSION postgis;" code
    docker compose exec db psql -U postgres -d mvc_test -c "CREATE EXTENSION IF NOT EXISTS postgis;"
```


- Install dependances

```bash

    python3 -m pip install -r requirements.txt

```


- Change directory

```bash

    cd src

```

- Initialize database

```bash

    flask db init 

```
- Generate migration

```bash

    flask db migrate 

```
- Upgrade database

```bash

    flask db upgrade 

```

- Load Data
```bash

    docker compose exec app flask load-data load-provinces ./data/provinces.json
    docker compose exec app flask load-data load-territories ./data/territories.json
    docker compose exec app flask load-data load-localities ./data/Localites.json

    docker compose exec app flask load-data load-existing-plant ./data/centrale_existantes_.geojson

    docker compose exec app flask load-data load-projects ./data/RDC_Centroides_RA_GEOJSON.geojson ./data/RDC_Rayons_d_action_GEOJSON.geojson


    
    docker compose exec app flask load-data load-provinces data/new_data/provinces26/Province26.shp
    docker compose exec app flask load-data load-territories data/new_data/territories/Territoire.shp
    docker compose exec app flask load-data load-project-excel-file data/new_data/projet_planifier.xlsx
    docker compose exec app flask load-data load-project-program-excel-file data/new_data/projet_programme.xlsx
    docker compose exec app flask load-data load-substation data/new_data/sous_stations/sous_stations.shp
    docker compose exec app flask load-data load-demands ./data/Territoires_Villes_Demande_potentielle_Menage_a_electrifier.GEOJSON
    docker compose exec app flask load-data load-health-zone data/new_data/zone_sante/OSM_RDC_sante_zones_211212.shp
    docker compose exec app flask load-data load-power-line  data/new_data/ligne_HT_existante/ligne_ht-line.shp
    docker compose exec app flask load-data load-power-line  data/new_data/ligne_MT_existante/grid_mt.shp

    docker compose exec app flask load-data load-health-instituttion2 data/new_data/structure_sante_2/GRID3_COD_health_facilities_v3_0.shp
    docker compose exec app flask load-data load-health-instituttion data/new_data/structure_sante/Structure_sante.shp


    docker compose exec app flask load-data load-substation-xlsx  data/noeud.xlsx
    docker compose exec app flask load-data load-power-line-xlsx data/ligne_existant.xlsx

```

## API

### Create Meta Data
- Description : Permet ds créer une entité avec tous les ces attributs et shema de valisation;
- Methede : `POST`
- En tête : 
  ```json
    {
        "Accept":"application/json",
        "Content-Type":"application/json",
    }

  ```
- Contenu de la requette :
  ```json
    {
        "name":"Anser.Demands.Population",
        "normalName":"Population",
        "geoType":"AUCUN",
        "props":[
            {
                "name":"pop",
                "type":"scalar"
            },
            {
                "name":"year",
                "type":"scalar"
            },
            {
                "name":"territory",
                "type":"relationship",
                "otherEntity":"Anser.EntityAdministration.Territory"
            }
        ],
        "schema":{
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties":{
                "pop": {
                    "type": "number"
                },
                "year": {
                    "type": "number"
                },
                "territory": {
                    "type": "number"
                }
            },
            "required": ["pop","year","territory"]

        }
    }

  ```
  - Reponse : un JSON qui represente l'entité
  ```json

    {
        "geo_type": "AUCUN",
        "id": 12,
        "name": "Anser.Demands.Population",
        "normalName": "Population",
        "props": [
            {
                "name": "pop",
                "type": "scalar"
            },
            {
                "name": "year",
                "type": "scalar"
            },
            {
                "name": "territory",
                "otherEntity": "Anser.EntityAdministration.Territory",
                "type": "relationship"
            }
        ],
        "schema": {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "properties": {
                "pop": {
                    "type": "number"
                },
                "territory": {
                    "type": "number"
                },
                "year": {
                    "type": "number"
                }
            },
            "required": [
                "pop",
                "year",
                "territory"
            ],
            "type": "object"
        }
    }
  ```

### Get all Meta Data
- Description : Permet de recupérer tous les entités créer;
- Methede : `GET`
- En tête : 
  ```json
    {
        "Content-Type":"application/json",
    }

  ```
  - Reponse : un JSON qui represente tous les entités
  ```json
    [
        {
            "geo_type": "AUCUN",
            "id": 12,
            "name": "Anser.Demands.Population",
            "normalName": "Population",
            "props": [
                {
                    "name": "pop",
                    "type": "scalar"
                },
                {
                    "name": "year",
                    "type": "scalar"
                },
                {
                    "name": "territory",
                    "otherEntity": "Anser.EntityAdministration.Territory",
                    "type": "relationship"
                }
            ],
            "schema": {
                "$schema": "http://json-schema.org/draft-07/schema#",
                "properties": {
                    "pop": {
                        "type": "number"
                    },
                    "territory": {
                        "type": "number"
                    },
                    "year": {
                        "type": "number"
                    }
                },
                "required": [
                    "pop",
                    "year",
                    "territory"
                ],
                "type": "object"
            }
        }

    ]

  ```

  ### Create Record
- Description : Permet d'enregistrer une donnée;
- Methede : `POST`
- En tête : 
  ```json
    {
        "Accept":"application/json",
        "Content-Type":"application/json",
    }

  ```
- Contenu de la requette :
  ```json
    {
        "metaName":"Anser.ExistingPlants.ExistingPlantType",
        "data":{
            "name":"Eolienne"
        }
    }
  ```
  - Reponse : un JSON qui represente l'enregistrement
  ```json
    {
        "createdAt": "Sun, 25 Aug 2024 07:18:28 GMT",
        "deletedAt": null,
        "geom": null,
        "id": 3,
        "props": {
            "name": "Eolienne"
        },
        "type_id": 8
    }

  ```

  ### Get data by meta data

- Description : Permet de récupérer les enregistrement d'un meta data;
- Methede : `POST`
- En tête : 
  ```json
    {
        "Accept":"application/json",
        "Content-Type":"application/json",
    }

  ```
- Contenu de la requette :
  ```json
    {
        "type":{
            "typeId":5
        }
    }
  ```

  - Reponse : un JSON qui represente les enregistrement
  ```json
    [
        {
            "createdAt": "Sun, 25 Aug 2024 07:18:28 GMT",
            "deletedAt": null,
            "geom": null,
            "id": 3,
            "props": {
                "name": "Eolienne"
            },
            "type_id": 8
        }
    ]
  ```

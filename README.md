## ETL pipeline of the USDA FoodData API with Python, PostgreSQL, Airflow and Docker Compose.

![image](https://drive.google.com/uc?export=view&id=1id7Bcieu9Bjt89Sz8eBxfUa0iFqkArIG)

USDA’s Economic Research Service (ERS) is making data from USDA’s Agricultural Resource Management Survey (ARMS) available through an Application Programming Interface (API) to better serve customers. The data in the API are available in JSON format and provide attribute-based querying.
In this case I am going to use Python's [requests](https://pypi.org/project/requests/) module to fetch the data for the ETL process.


### Pre-requisites:
1. Register to get the ERS API key on [https://www.ers.usda.gov/developer/data-apis/#apiForm]
  

### Setup the environment:

1. Create .env file with the environment variables described below:

```

# Meta-Database

POSTGRES_USER=airflow

POSTGRES_PASSWORD=airflow

POSTGRES_DB=airflow


# Airflow Core

AIRFLOW__CORE__FERNET_KEY=UKMzEm3yIuFYEq1y3-2FxPNWSVwRASpahmQ9kQfEr8E=

AIRFLOW__CORE__EXECUTOR=LocalExecutor

AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION=True

AIRFLOW__CORE__LOAD_EXAMPLES=False

AIRFLOW_UID=0

  
# Backend DB

AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres/airflow

AIRFLOW__DATABASE__LOAD_DEFAULT_CONNECTIONS=False


# Airflow Init

_AIRFLOW_DB_UPGRADE=True

_AIRFLOW_WWW_USER_CREATE=True

_AIRFLOW_WWW_USER_USERNAME=airflow

_AIRFLOW_WWW_USER_PASSWORD=airflow

```

2. Aditionally, set the **required** environment variables for the database and the Docker volumes:

- API key:

`USDA_API_KEY`


- ETL database:

`_POSTGRES_DB`

`_POSTGRES_USER`

`_POSTGRES_PASSWORD`

`_POSTGRES_HOST`

`_POSTGRES_PORT`


- Volumes:

`PG_DATA`

  
#### Postgresql

1. ``$ docker network create etl_network``

2. ``$ docker-compose --env-file ./.env -f ./postgres-docker-compose.yaml up -d``


#### Airflow

1. ``$ docker build -f airflow-dockerfile .``

2. ``$ docker-compose -f airflow-docker-compose.yaml up -d``


#### Airflow Webserver

1. Go to [http://localhost:8080/] and login with the default Airflow credentials:

```
Username: airflow
Password: airflow
```

2. In the DAGs list you will see a DAG called *af_foods.py* with the graph as shown below:

![image](https://drive.google.com/uc?export=view&id=182_LUg_GEdE5CM3muXZNDkteB7RQn1HT)

#### Clean Up

To stop and remove all the containers, including the bridge network, run the following command:

```

docker-compose -f postgres-docker-compose.yaml down --volumes --rmi all

docker-compose -f airflow-docker-compose.yaml down --volumes --rmi all

docker network rm etl_network

```
## Data Change Capture from database Postgresql to S3
### Configuring PostgreSQL for CDC
- Enable Logical Replication: Modify parameters in file `postgresql.conf`:
` vim /usr/local/var/postgresql@14/postgresql.conf`
```
wal_level = logical
max_replication_slots = 4
max_wal_senders = 4
```
- Create Database and Table using `psql` or `pgadmin`:
+ `CREATE DATABASE cdc_example;`
+ `CREATE TABLE public.users (
   id SERIAL PRIMARY KEY,
   name VARCHAR(100),
   email VARCHAR(100)
);`

+ `CREATE TABLE public.orders (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES public.users(id),
    total DECIMAL(10, 2)
);`

- Create a Publication: `CREATE PUBLICATION my_publication FOR TABLE public.users, public.orders;`
- Create a User with Replication Privileges:
+ Create the user:`CREATE USER cdc_user WITH PASSWORD 'your_password' REPLICATION;`
+ Grant access to the database: `GRANT CONNECT ON DATABASE cdc_example TO cdc_user;
GRANT USAGE ON SCHEMA public TO cdc_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO cdc_user;
`
### Config Kafka sever
- Check ip : `ipconfig getifaddr en0`
- Modify file `sever.properties` in kafka: `vim /usr/local/etc/kafka/server.properties`:
     + `advertised.listeners=PLAINTEXT://<ip_adress>:9092`
- Stop and restart:
     + `brew services stop kafka`
     + `brew services restart kafka`
- Check topic Kafka: `kafka-topics --list --bootstrap-server localhost:9092`
- Check message topic: `/usr/local/Cellar/kafka/3.8.0/libexec/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic <topic-name> --from-beginning`
- Delete topic Kafka: `/usr/local/Cellar/kafka/3.8.0/libexec/bin/kafka-topics.sh --delete --topic <topic_name> --bootstrap-server localhost:9092`
`

### Config Kafka Connect using Docker
- Modify .env file: Minion S3, Kafka, Topic default information
- Create file: `docker-compose.yaml`
- Run project: `docker-compose up -d`
- Source connector: `curl -X POST -H "Content-Type: application/json" --data @./connector/postgres-source-connector.json http://localhost:8083/connectors`
- Sink connector: `curl -X POST -H "Content-Type: application/json" --data @./connector/s3-sink-config.json http://localhost:8083/connectors`
- Test source-connector and sink-connector table 1 million row:
   + `python test.py`
   + `curl -X POST -H "Content-Type: application/json" --data @./connector/postgres-source-connector-test.json http://localhost:8083/connectors`
   + `curl -X POST -H "Content-Type: application/json" --data @./connector/s3-sink-connector-test.json http://localhost:8083/connectors`
- Test sink-connector database mysql:
   + `curl -X POST -H "Content-Type: application/json" --data @./connector/mysql-sink-connector.json http://localhost:8083/connectors`
### Connector Kafka-Connect:
- List all connector running: `curl -X GET http://localhost:8083/connectors`
- Check status a connector: `curl -X GET http://localhost:8083/connectors/<connector-name>/status`
- Check config a connector: `curl -X GET http://localhost:8083/connectors/<connector-name>/config`
- Delete a connector: `curl -X DELETE http://localhost:8083/connectors/<connector-name>`


### Configuring Mysql for CDC
- Modify `my.cnf` file mysql config:
```commandline
vim /usr/local/etc/my.cnf
bind-address
```

- Restart mysql: `brew services restart mysql`
- Error connection ip: https://stackoverflow.com/questions/19101243/error-1130-hy000-host-is-not-allowed-to-connect-to-this-mysql-server
- Check history terminal: `cat ~/.zsh_history`
- `docker exec -it kafka-connect ls /kafka/connect/`
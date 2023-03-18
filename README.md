# Test task for an inteview in OKKAM

## Initialization

```console
$ docker-compose build
```

## Running the web application

```console
$ docker-compose up
```

## API usage

```console
$ curl -X GET localhost/getPercent -d '{"audience1": "age BETWEEN 20 and 40", "audience2": "age > 30 AND sex = 2"}'
{"percent": 0.282341350771364}
```

## Troubleshooting

1.  Rebuild and restart docker containers.

2.  Check if table `audience` is filled successfully:
    ```console
    $ docker exec -it okkamtestapp-db-1 psql -U okkam -d okkam -c "SELECT COUNT (*) FROM audience"
     count  
    --------
     500000
    (1 row)
    ```

    If the table is empty, fill it manually:
    ```console
    $ docker exec -it okkamtestapp-db-1 psql -U okkam -d okkam -c "COPY audience(id, date, respondent_id, respondent_sex, respondent_age, weight) FROM '/etc/OKKAM_Middle Python Developer_data.csv' DELIMITER ';' CSV HEADER"
    COPY 500000
    ```

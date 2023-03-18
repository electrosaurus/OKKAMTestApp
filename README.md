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
# bff-python-template
 :snake: Python based
 :strawberry: Strawberry based 
 :seedling: Postgres
 :broom: CleanArchitecture

## Quickstart
```
docker compose up
```

## Migration
```
docker-compose -f docker-compose.migration.yml up
docker exec -it bff-python-template-api-1 bash
```

To create a new version (for example, "create tables"), 
```
$ alembic revision --autogenerate -m "create tables"
```
To check where we are
```
alembic current
```
To upgrade head / +1
```
alembic upgrade head/+1
```
To downgrade base / -1
```
alembic downgrade base/-1
```


## Reference
 - [PythonのGraphQLライブラリStrawberryを使ってみた](https://qiita.com/nttpc-aiyo/items/bb946b864e67c2da9a53)
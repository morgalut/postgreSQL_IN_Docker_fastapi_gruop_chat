## build docker
```docker-compose up -d```

## build Database
```docker-compose exec postgres1 psql -U postgres
```

## Curl Test

``` curl -X POST http://localhost:8000/users/ -H "Content-Type: application/json" -d "{\"username\":\"new_user\", \"email\":\"new_user@example.com\"}" ```

```curl -X GET http://localhost:8000/users/```
``` curl -X POST http://localhost:8000/messages/ -H "Content-Type: application/json" -d "{\"user_id\":1, \"content\":\"Hello, World!\"}" ```
``` curl -X GET http://localhost:8000/messages/ ```

Third party services
```
docker-compose up -d
```

Start server
```
poetry run server
```


Run tests
```
poetry run pytest
```

Generate RSA keys 
```
docker run --rm oryd/oathkeeper:v0.38.20-beta.1 credentials generate --alg RS256 --kid test-str > keys/jwks.json
```

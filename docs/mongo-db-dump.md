---
layout: default
title: MongoDB Dump
---

## Env variables
If you are on Linux/Ubuntu you can export you env variables into system by command 
1. Export env variables (Optional):
```
export $(cat .env | xargs)
```

## Dump
1. Run dump command inside the container (If you don't have env variables please just insert values)
```
docker-compose exec mongo-db mongodump --archive=/data/dump.gz --gzip --db $MONGO_DATABASE --username $MONGO_USERNAME --password $MONGO_PASSWORD --authenticationDatabase admin
```
2. Copy dump file from docker container into host
```
docker cp tg_chat_mate-mongo-db-1:/data/dump.gz ./dump.gz
```

## Restore from dump

1. Copy dump file into container from host:
```
docker cp ./dump.gz tg_chat_mate-mongo-db-1:/data/dump.gz
```
2. Run restore command from docker inside docker container (If you don't have env variables please just insert values)
```
docker-compose exec mongo-db mongorestore --archive=/data/dump.gz --gzip --db $MONGO_DATABASE --username $MONGO_USERNAME --password $MONGO_PASSWORD --authenticationDatabase admin
```






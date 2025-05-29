# Task6
___
This program contains methods to save and get urls from DB using Docker containers.

### Program usage
* To start app run:
``` commandline
docker-compose up -d --build
```
* To save url run:
```commandline
curl "http://localhost:80/parse?url={url}"
```
replace {url} with the obe you want to save
* To get DB data run:
```commandline
curl http://localhost:80/data
```
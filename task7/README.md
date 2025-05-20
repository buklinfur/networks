# Task6
___
This program contains methods to save and get urls from DB using Docker containers.

## Available [here](https://link-url-here.org)

### Program usage
* Run the PostgreSQL server.
* To start app run:
``` commandline
docker-compose up -d
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
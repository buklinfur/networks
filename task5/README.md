# Task5
___
This program contains methods to save and get urls from DB using Docker containers.

### Program usage
* Run the PostgreSQL server.
* To start network run:
``` commandline
docker network create app-network 
```
* To raise DB Docker run:
```commandline
docker build -t url-db -f db/Dockerfile.db . 

docker run -d --name db --network app-network -v pgdata:/var/lib/postgresql/data url-db
```
* To raise app Docker run:
```commandline
docker build -t url-app . 

docker run -d --name app --network app-network -p 5000:5000 url-app  
```
* To save url run:
```commandline
curl "http://localhost:5000/parse?url={url}"
```
replace {url} with the obe you want to save
* To get DB data run:
```commandline
curl http://localhost:5000/data
```
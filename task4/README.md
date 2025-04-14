# Task 4
___
This program raises api endpoints for minecraft servers parser

### Program usage
* Run the PostgresSQL server. (Replace DB name, table name etc. in ```app.py``` or use the same.)
* Run the python script: ```py app.py```
  * To close connection press ctrl+c
* To parse particular page run: 
``` cmd
curl "http://localhost:5000/parse?url=https://minecraftservers.org/index/{page}" 
```
replace {page} with a number of page you want to parse.
* To get the data from DB run:
``` cmd
curl http://localhost:5000/data  
```
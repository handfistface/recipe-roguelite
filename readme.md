
# TODO
- my own recipe database
- weekly recipe generation/on demand?
- grocery list generation
- list with add/delete system
- weekly standalone items to get when you generate your grocery list

# Setup
1. Create a file for the database connection. `lib/db_config.py`. It's contents should be the following: ```db_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'REPLACE_WITH_PWD',
    'database': 'recipe-roguelite'
}```
1. Run your mySql instance in podman `podman run --name docker.io-library-mysql -e MYSQL_ROOT_PASSWORD=REPLACE_WITH_PWD -p 3306:3306 -d mysql:oraclelinux9`. Note that I pulled the image from [this registry](https://hub.docker.com/_/mysql)
1. Install your libraries for python `pip install -r requirements.txt`

# Podman debugging
## Getting IP Address of Pod
```
podman inspect -f '{{.NetworkSettings.IPAddress}}' <container_name_or_id>
podman inspect -f '{{.NetworkSettings.IPAddress}}' e5493eb86fc4
podman ps -a
```
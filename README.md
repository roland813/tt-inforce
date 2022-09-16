# Lunch_service

## Instalation

### Python and PostgreSQL must be already installed !

```shell
git clone https://github.com/roland813/tt-inforce
python3 -m venv venv
venv/Scripts/activate
pip install -r requirments.txt
export/set DB_HOST=<host name>
export/set DB_NAME=<db name>
export/set DB_USER=<user name>
export/set DB_PASSWORD=<db password>
python manage.py migrate
python manage.py runserver
```

### To use Docker:
```shell
docker-compose build
docker-compose up
```

### To read documentation:
Endpoint to swagger/ and redoc/
```
127.0.0.1:8000/api/doc/swagger/
127.0.0.1:8000/api/doc/redoc/
```
To build and run django app and postgres DB
```
docker-compose up --build -d
```

To run django migrations
```
docker-compose exec accuknox_django python manage.py makemigrations
docker-compose exec accuknox_django python manage.py migrate
```

Postman collection

```
https://api.postman.com/collections/11320669-299cc3ea-26ce-4f21-86fe-96d1f7aaab9a?access_key=PMAT-01HCX311R20CCP9THC97Q2K0WM
```
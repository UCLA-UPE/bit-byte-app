# bit-byte-app

# Installation
1. Make sure you have docker (with docker-compose installed)

https://docs.docker.com/docker-for-mac/install/

https://docs.docker.com/docker-for-windows/install/

2. Run the following to start server:

```
docker-compose up # starts server on localhost:8000

# Ctrl+c to shut down the server
```

# Starting terminal in server and creating admin account

To run anything django-related management commands, you need to start a shell in the docker.
Make sure you have started the server with step 2, and run the following:

```
docker-compose exec web sh
```

Next, to create an admin account, run the following in the shell above:

```
python manage.py createsuperuser
```

Now you can use this to navigate to /admin to log into the admin page.

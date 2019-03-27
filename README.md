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
Make sure you have started the server with step 2, and run the following (in another window):

```
docker-compose exec web sh
```

Next, to create an admin account, run the following in the shell above:

```
python manage.py createsuperuser
```

Now you can use this to navigate to /admin to log into the admin page.

# Design

Please look at models.py for the data model.

At a high level:
1. Profile contains the metadata for each user, and has a one-to-one key to users. This meta data includes whether they are a 
bit or byte, and their answers to the bit-byte questions (in JSON format).

2. Choice contains all the choices of bits and bytes, with two foreign keys designating the "chooser" and "choosee". Suppose user1 chooses user2 and user3. Then this table may contain two entries with foreign keys chooser and choosee as follows:

chooser: user1, choosee: user2

chooser: user1, choosee: user3

There's also a "finalized" boolean flag to indicate if this choice is the choice that should be used. The eventual matching algorithm should deal with this.

3. SiteSettings contains all the site specific parameters. These include special keys for bits and bytes, which must be used in order to sign up. The questions for the quarter (which should be the same for bits and bytes), will also be the same.

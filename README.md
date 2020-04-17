# bit-byte-app

# Installation
0. This should be run on an AWS instance. Options for creating a fresh dashboard: (1) create new aws instance, (2) remove everything from previous instance
using ./manage.py dbshell after sshing to the web shell admin account (after step 2).

Create new instance on AWS - can use free tier as of 4/16/2020. Expose 0.0.0.0/, ::00 for HTTP (80) and HTTPS (443) in security groups

Install git on ec2:

```
sudo yum install git -y
```

Install docker, docker-compose on ec2:

https://docs.aws.amazon.com/AmazonECS/latest/developerguide/docker-basics.html
```
sudo curl -L https://github.com/docker/compose/releases/download/1.21.0/docker-compose-`uname -s`-`uname -m` | sudo tee /usr/local/bin/docker-compose > /dev/null
sudo chmod +x /usr/local/bin/docker-compose
```

1. Make sure you have docker (with docker-compose installed) if you're doing it locally

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

# Design (Below may be outdated)

https://github.com/austinguo550/byteBitWebpageFlowDiagrams

# Technical Design

This project has been laid out in accordance with standard Django practices. Please look at models.py for the data model. For basic Django resources, refer to the documentation, and https://docs.djangoproject.com/en/2.1/intro/tutorial01/ which is very similar to this project.

```
.
├── Dockerfile
├── bitbyte
│   ├── __init__.py
│   ├── settings.py <- Django settings for website
│   ├── urls.py <- toplevel routing, which will direct / to internal/urls.py
│   └── wsgi.py
├── docker-compose.yml
├── docker-entrypoint.sh
├── internal
│   ├── __init__.py
│   ├── admin.py <- file to register models into admin panel
│   ├── apps.py
│   ├── models.py <- data models
│   ├── tests.py
│   ├── urls.py <- routing for main app (to connect urls to views)
│   └── views.py <- views for main app
├── manage.py <- main entrypoint, which you probably won't need
└── requirements.txt
```

At a high level:
1. __Profile__ contains the metadata for each user, and has a one-to-one key to users. This meta data includes whether they are a bit or byte, and their answers to the bit-byte questions (in JSON field), as list of strings. These correspond to the questions in SiteSettings (explained below).

2. __Choice__ contains all the choices of bits and bytes, with two foreign keys designating the "chooser" and "choosee". Suppose user1 chooses user2 and user3. Then this table may contain two entries with foreign keys chooser and choosee as follows:

chooser: user1, choosee: user2

chooser: user1, choosee: user3

There's also a "finalized" boolean flag to indicate if this choice is the choice that should be used. The eventual matching algorithm should deal with this.

3. __SiteSettings__ contains all the site specific parameters. These include special keys for bits and bytes, which must be used in order to sign up. The questions for the quarter (which should be the same for bits and bytes), are also in here, in JSON field, as a list of strings. Each person's answer in the ith index correspond to the question in the ith index.

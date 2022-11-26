- [Installation](#installation)

### Installation

#### Clone repo

``` bash
# clone the repo
$ git clone 'https://github.com/Huxteen/green-energy-api.git'

# go into app's directory
$ cd green-energy-api

# Build docker-compose
$ docker-compose build

## Run test and Flake8
$ docker-compose run app sh -c "python manage.py test && flake8"

# start project
$ docker-compose up

# API Documentation Endpoint
 {{base_url}}/swagger/schema/

 # Create Super User
 $ docker-compose run app sh -c "python manage.py createsuperuser"





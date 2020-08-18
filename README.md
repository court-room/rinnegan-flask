# rinnegan-flask

[![test Actions Status](https://github.com/court-room/rinnegan-flask/workflows/test/badge.svg)](https://github.com/court-room/rinnegan-flask/actions)
[![docker Actions Status](https://github.com/court-room/rinnegan-flask/workflows/docker/badge.svg)](https://github.com/court-room/rinnegan-flask/actions)
[![DeepSource](https://static.deepsource.io/deepsource-badge-light-mini.svg)](https://deepsource.io/gh/court-room/rinnegan-flask/?ref=repository-badge)
[![Dependabot Status](https://api.dependabot.com/badges/status?host=github&repo=court-room/rinnegan-flask)](https://dependabot.com)

## Pre-Requisite

Run the following commands for setting up the dependencies of your server

- Create the networks with the given name

  ```bash
  $ docker network create --attachable rinnegan-database
  $ docker network create --attachable rinnegan-backend
  ```

- Create a volume with the given name

  ```bash
  $ docker volume create rinnegan-data
  ```

## Setup

The server can be used for locally testing the client or the entire set of services.
In order to use the server you need a dependency on the database, which is defined in the compsoe file.

- Make sure you have a copy of `.env` file created by using `.env.example` as a template

- Build the image

  ```bash
  $ docker-compose build --compress
  ```

- Launch the container

  ```bash
  $ docker-compose up --detach
  ```

## Development

- In order to verify that the container is up

```bash
$ docker container ls
```

- To open the Swagger API Explorer please open a browser and go to `http://localhost:5000`

## Contact

For any issue please contact the following persons

- [onlinejudge95](https://github.com/onlinejudge95)

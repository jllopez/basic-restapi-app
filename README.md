# Basic REST API Application using FastAPI

Naive solution for a basic REST API application. Its main purpose is to provide an easy way to expose endpoints and enable SDETs to build automation frameworks around it.

The application was designed to run inside a `Docker` container to strip out the complexity of setting virtual environments, facilitate its distribution and avoid the infamous ***but it works on my machine*** conversation.

## Prerequisites

- [Git](https://git-scm.com/downloads)
- [Docker](https://www.docker.com/products/docker-desktop)
- [Make](https://discussions.apple.com/thread/1404907)

## Run the App

1. Open a terminal

2. Change to your favorite local directory (i.e. `cd /opt`)

3. Clone the repository

```bash
git clone git@github.com:jllopez/basic-restapi-app.git
```

4. Run the application

```bash
make run
```

> This command will remove any existing `fastapi_restapp` containers and build a new `dev/fastapi_restapp` image.

5. Visit URL

```bash
http://localhost:8080/docs#/
````

> User `admin/admin` is preloaded in the DB. Leverage this user to authenticate and perform admin-only operations (i.e. create/delete/list-all users, delete comments)

## Developer Mode

1. Complete steps 1-3 as described in [Run the App](#run-the-app) section.

2. Start development environment

```bash
make dev
```

> This command will remove any existing `fastapi_restapp` containers, build a new `dev/fastapi_restapp` image, start a container, mount local code under `/opt/app` and provide a `/bin/bash` terminal.

3. Start uvicorn server by executing the following command in the container's terminal

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

Now the container is ready for development. Local code changes will be automatically reflected inside the container and thanks to the `--reload` uvicorn flag the code will be immediately deployed.

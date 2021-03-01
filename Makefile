# Container's default name
NAME=fastapi_restapp

# Docker image default name
IMAGE=dev/$(NAME)

# Mount localfile system for local development
LOCAL_OPTS=-v $(shell pwd):/opt -e PYTHONPATH="/opt/app"

# Build image
.PHONY: build
build:
	@echo "--> Building $(NAME)"
	docker build -t $(IMAGE) .

# Stop container
.PHONY: stop
stop:
	@echo "--> Stopping $(NAME)"
	docker kill $(NAME) || true

# Start container
.PHONY: start
start:
	@echo "--> Starting $(NAME)"
	docker start $(NAME)

# Remove container
.PHONY: rm
rm:
	@echo "--> Removing container $(NAME)"
	docker rm -f $(NAME) || true

# Tail container logs
.PHONY: logs
logs:
	docker logs -f $(NAME)

# Run container and provide a Shell terminal
.PHONY: local
local:
	@echo "--> Starting $(NAME)"
	docker run $(LOCAL_OPTS) --name $(NAME) -p 8080:8080 -it $(IMAGE) /bin/bash

# Local development
.PHONY: dev
dev: stop rm build local

# Run container and start the application using uvicorn
.PHONY: server
server:
	@echo "--> Starting $(NAME)"
	docker run $(LOCAL_OPTS) --name $(NAME) -p 8080:8080 -it $(IMAGE) uvicorn app.main:app --host 0.0.0.0 --port 8080

# Run the application
.PHONY: run
run: stop rm build server

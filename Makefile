# Variables
DOCKER_COMPOSE = docker-compose
DOCKER_COMPOSE_FILE = docker-compose.yml


# Executables (local)
DOCKER_COMP = docker-compose
DOCKER = docker

# Docker containers
PHP_CONT = $(DOCKER_COMP) exec php

# Misc
.DEFAULT_GOAL = help
.PHONY        : help build up start down logs sh composer vendor sf cc test

## —— 🎵 🐳 The Symfony Docker Makefile 🐳 🎵 ——————————————————————————————————
help: ## Outputs this help screen
	@grep -E '(^[a-zA-Z0-9\./_-]+:.*?##.*$$)|(^##)' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}{printf "\033[32m%-30s\033[0m %s\n", $$1, $$2}' | sed -e 's/\[32m##/[33m/'

## —— Docker 🐳 ————————————————————————————————————————————————————————————————
build-prod: ## Builds the Docker images
	@$(DOCKER_COMP) -f docker-compose.yaml build --no-cache

login: ## Starts the Docker containers
	echo "dckr_pat_EH77V0Pe_KGxXKKgYzWjaGnWC1c" | docker login -u mdnicolae --password-stdin

push: ## Pushes the Docker images
	docker push mdnicolae/rmy.bg:latest

upload-prod: stop remove-containers login build-prod push

ssh-ec2:
	ssh -i "portofolio2.pem" ec2-user@ec2-16-171-76-136.eu-north-1.compute.amazonaws.com

stop:
	@$(DOCKER_COMP) stop
remove-containers:
	docker container ls -aq | xargs --no-run-if-empty docker container rm -f
build-local:
	@$(DOCKER_COMP) build --no-cache
up-local:
	@$(DOCKER_COMP) up -d
local: stop remove-containers build-local up-local


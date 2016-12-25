NAME=hopper

build:
	docker-compose build ${NAME}

bash: build
	docker-compose run --rm ${NAME} /bin/bash

run: build
	docker-compose run -p 8000:8000 --rm ${NAME} bin/run

migrations:
	docker-compose run --rm ${NAME} django-admin makemigrations ${NAME}

migrate:
	docker-compose run --rm ${NAME} django-admin migrate ${NAME}

static: build
	docker-compose run --rm ${NAME} django-admin collectstatic --noinput

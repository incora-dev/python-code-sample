#!/bin/bash
export USERS_APP_NAME="users-db"
export USERS_DB_NAME="users_db"
export USERS_DB_PASSWORD="users_db_password"
export USERS_DB_USER="users_db_admin"
export USERS_DB_HOST="0.0.0.0"
export USERS_DB_PORT="5433"
export USERS_DB_PORT_EXT="5433"
export PROJECTS_APP_NAME="projects-db"
export PROJECTS_DB_NAME="projects_db"
export PROJECTS_DB_PASSWORD="projects_db_password"
export PROJECTS_DB_USER="projects_db_admin"
export PROJECTS_DB_HOST="0.0.0.0"
export PROJECTS_DB_PORT="5434"
export PROJECTS_DB_PORT_EXT="5434"
export MAIN_APP_DIR="main-app"
export MAIN_APP_NAME="main-app"
export MAIN_APP_PORT_EXT="8001"
export MAIN_APP_PORT="8000"
export SECRET_KEY="_xmda456_)!li)*-iw0"
export DEBUG="True"
export LANGUAGE_CODE="en-US"
export TIME_ZONE="UTC"
export DOCKER_ENV_NAME="development"
export DOCKER_COMPOSE_FILE="scripts/docker_scripts/docker-compose.yml"
export SUPERUSER_NAME="admin"
export SUPERUSER_PASSWORD="super-password"
export SUPERUSER_EMAIL="admin@admin.com"
export DEFAULT_DOCKER_HOST="0.0.0.0"
export ADMIN_EMAIL="admin@admin.com"
export DATABASES_APP_NAME="databases"

export ALLOWED_HOST="0.0.0.0"

if [[ $1 ]]; then
	python manage.py $1 $2
else
	python manage.py runserver 0.0.0.0:8000
fi

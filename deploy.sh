#!/bin/bash

# Генерируем файл .env на основе шаблона, передав внутрь название окружения
bash ./generate.env.sh $CI_ENVIRONMENT_NAME

# Копируем необходимые для запуска контейнеров файлы в папку проекта
sudo cp -r ./nginx $BACKEND_FOLDER
sudo cp ./.env $BACKEND_FOLDER
sudo cp ./docker-compose.yml $BACKEND_FOLDER

# Переходим в папку проекта
cd $BACKEND_FOLDER

# Обновляем контейнеры
docker-compose down --remove-orphans
docker login -u gitlab-ci-token -p $CI_JOB_TOKEN $CI_REGISTRY
docker pull $CI_REGISTRY_IMAGE:$CI_ENVIRONMENT_NAME
docker-compose up -d
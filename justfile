# Список команд
default:
  just --list
  
# Запуск Django
django:
    python manage.py runserver

# Запуск Redis у Docker
redis:
    docker start redis || docker run -d --name redis -p 6379:6379 redis:7-alpine

# Запуск Celery Worker
celery-worker:
    celery -A core worker -l info

# Запуск Celery Beat Worker
beat-worker:
    celery -A core beat -l info

# Створення періодичних задач
setup-periodic-tasks:
    python manage.py setup_periodic_tasks

# Видалення періодичних задач
clear-periodic-tasks:
    python manage.py clear_periodic_tasks

# Створення міграції
migrate:
    python manage.py makemigrations
    python manage.py migrate

# Запуск Django + Celery Worker + Celery Beat Worker
run:
    bash -c '\
      python manage.py runserver & \
      celery -A core worker -l info & \
      celery -A core beat -l info & \
      wait'

# Запуск усіх Docker-контейнерів
docker-up:
    docker compose up -d

# Перебудова образів та запуск усіх Docker-контейнерів
docker-up-build:
    docker compose up -d --build

# Зупинка Docker-контейнерів
docker-down:
    docker compose down

# Перезапуск Docker-контейнерів
docker-restart:
    docker compose restart

# Перегляд статусу Docker-контейнерів
docker-ps:
    docker compose ps

# Перегляд логів усіх Docker-контейнерів
docker-logs:
    docker compose logs -f

# Перегляд логів Django
docker-logs-web:
    docker compose logs -f web

# Перегляд логів Celery Worker
docker-logs-celery:
    docker compose logs -f celery

# Перегляд логів Celery Beat
docker-logs-celery-beat:
    docker compose logs -f celery-beat

# Виконання Django-команди всередині контейнера
docker-manage command:
    docker compose exec web python manage.py {{command}}

# Створення міграцій у Docker
docker-makemigrations:
    docker compose exec web python manage.py makemigrations

# Застосування міграцій у Docker
docker-migrate:
    docker compose exec web python manage.py migrate

# Створення суперкористувача у Docker
docker-createsuperuser:
    docker compose exec web python manage.py createsuperuser

# Запуск Django shell у Docker
docker-shell:
    docker compose exec web python manage.py shell

# Відкрити bash у Django-контейнері
docker-bash:
    docker compose exec web bash
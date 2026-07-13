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
setup-tasks:
    python manage.py migrate
    python manage.py setup_periodic_tasks

# Запуск Django + Celery Worker + Celery Beat Worker
run:
    bash -c '\
      python manage.py runserver & \
      celery -A core worker -l info & \
      celery -A core beat -l info & \
      wait'
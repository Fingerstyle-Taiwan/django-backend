build:
	@docker-compose build

up:
	@docker-compose up

down:
	@docker-compose down

superuser:
	@docker-compose run --rm django-app sh -c "python3 manage.py createsuperuser"

create-app:
	@docker-compose run --rm django-app sh -c "django-admin startapp $(NAME)"

migrations:
	@docker-compose run --rm django-app sh -c "python manage.py makemigrations"

migrate-init:
	@docker-compose run --rm django-app sh -c "python manage.py migrate --fake-initial"

migrate:
	@docker-compose run --rm django-app sh -c "python manage.py migrate"

database-init:
	@docker-compose down --volumes

test:
	@docker-compose run --rm django-app sh -c "python manage.py test"

lint:
	@docker-compose run --rm django-app sh -c "black . && isort . && flake8"

check:
	make test && make lint

prod-up:
	@docker-compose -f docker-compose-deploy.yml up -d

prod-superuser:
	@docker-compose -f docker-compose-deploy.yml run --rm app sh -c "python3 manage.py createsuperuser"

prod-down:
	@docker-compose -f docker-compose-deploy.yml down

prod-init:
	@docker-compose -f docker-compose-deploy.yml down --volumes

prod-logs:
	@docker-compose -f docker-compose-deploy.yml logs

prod-rebuild:
	@docker-compose -f docker-compose-deploy.yml build app

prod-re-up:
	@docker-compose -f docker-compose-deploy.yml up --no-deps -d app
monitor-up:
	@docker-compose -f docker-compose-monitor.yml up 
monitor-down:
	@docker-compose -f docker-compose-monitor.yml down
certbot-init:
	@docker-compose -f docker-compose-deploy.yml run --rm certbot /opt/certify-init.sh
 
web: gunicorn run:app --log-level=debug

init: python db_create.py
upgrade: python db_migrate.py; python db_upgrade.py
worker: rq worker -u $REDIS_URL menta4-tasks
web2: gunicorn app:app --log-level=debug

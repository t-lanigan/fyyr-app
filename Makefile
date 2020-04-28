APP_NAME := fyyr

deps:
	pip3 install -r requirements.txt

run:
	FLASK_APP=app.py FLASK_DEBUG=true flask run

reset-db:
	dropdb $(APP_NAME) && createdb $(APP_NAME)
	flask db upgrade
	python add_fake_data.py

start-db-server:
	pg_ctl -D /usr/local/var/postgres start

stop-db-server:
	pg_ctl -D /usr/local/var/postgres stop

connect-to-db:
	psql $(APP_NAME)

delete-venue:
	curl -X DELETE http://localhost:5000/venues/1
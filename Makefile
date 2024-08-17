SHELL := /bin/bash

install:
	python3.10 -m venv venv && \
	source venv/bin/activate && \
	pip install --upgrade pip && \
	pip install --upgrade setuptools 

run:
	python app.py

build:
	docker build -t geospatial-api . && \
	docker compose -f docker-compose.yml up -d && \ 
	docker run -d --name geo-api -p 5000:5000 geospatial-api && \
	make create_db

create_db:
	@echo "Verifying if database geodata exists..."
	@if [ -z "$$(psql -h localhost -U postgres -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='geodata'")" ]; then \
		echo "Database geodata does not exist. Creating..."; \
		psql -h localhost -U postgres -d postgres -c "CREATE DATABASE geodata"; \
	else \
		echo "Database geodata already exists."; \
	fi

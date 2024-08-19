SHELL := /bin/bash

install:
	python3.10 -m venv venv && \
	source venv/bin/activate && \
	pip install --upgrade pip && \
	pip install --upgrade setuptools && \
	pip install -e .[all]

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

make test_geometry:
	cd .. && \
	python -m unittest geospatial_api.tests.test_geometry

make test_adress:
	cd .. && \
	python -m unittest geospatial_api.tests.test_adress

install_docker:
	sudo apt update && \
    sudo apt install -y apt-transport-https ca-certificates curl software-properties-common && \
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu focal stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null && \
    sudo apt update && \
    sudo apt install -y docker-ce docker-ce-cli containerd.io

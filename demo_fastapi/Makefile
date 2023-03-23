include .env
export $(shell sed 's/=.*//' .env)

setup:
	cp .env.example .env && \
	python3 -m venv venv && \
	. venv/bin/activate && \
	pip install --upgrade pip && \
	pip install --no-cache-dir --upgrade -r requirements.txt

run-app:
	uvicorn main:app --reload

build:
	docker build -t demo-fastapi:latest .

run:
	docker run  --name demo-fastapi -d -p 8000:8000 demo-fastapi:latest

destroy:
	docker rm demo-fastapi --force

build-and-run:
	docker build -t demo-fastapi:latest . && \
	docker run  --name demo-fastapi -d -p 8000:8000 demo-fastapi:latest

dc-up:
	docker-compose up -d

dc-down:
	docker-compose down

db-test:
	python db_test.py
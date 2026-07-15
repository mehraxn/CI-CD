# TaskOps — local quality, security, and ops gates.
# Usage: make <target>   (run `make help` to list targets)

# Use the project virtualenv if present, otherwise fall back to PATH tools.
VENV_BIN := .venv/bin
ifeq ($(OS),Windows_NT)
	VENV_BIN := .venv/Scripts
endif

PYTHON := $(VENV_BIN)/python
PIP    := $(PYTHON) -m pip

IMAGE ?= taskops:latest

.DEFAULT_GOAL := help

.PHONY: help install run test lint format format-check security audit check \
        docker-build compose-up compose-down clean

help: ## List available targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Create venv (if needed) and install dev requirements
	python -m venv .venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements-dev.txt

run: ## Run the app with the Flask dev server
	$(PYTHON) wsgi.py

test: ## Run the pytest suite
	$(PYTHON) -m pytest

lint: ## Static checks with ruff
	$(VENV_BIN)/ruff check .

format: ## Auto-format with black and isort
	$(VENV_BIN)/black .
	$(VENV_BIN)/isort .

format-check: ## Verify formatting without writing changes
	$(VENV_BIN)/black --check .
	$(VENV_BIN)/isort --check-only .

security: ## Scan source for security issues with bandit
	$(VENV_BIN)/bandit -r app

audit: ## Audit pinned dependencies for known CVEs
	$(VENV_BIN)/pip-audit -r requirements.txt

check: lint format-check test security audit ## Run all quality + security gates

docker-build: ## Build the container image
	docker build -t $(IMAGE) .

compose-up: ## Start the stack with docker compose
	docker compose up -d --build

compose-down: ## Stop and remove the docker compose stack
	docker compose down

clean: ## Remove caches, build artifacts, and local SQLite files
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	rm -rf .pytest_cache .ruff_cache .mypy_cache .coverage htmlcov \
		build dist *.egg-info
	rm -f *.db *.sqlite *.sqlite3 *.log

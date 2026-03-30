.PHONY: help install install-dev test test-cov lint format type-check clean

help:
	@echo "Personal History - Development Commands"
	@echo ""
	@echo "install      Install package in development mode"
	@echo "install-dev  Install development dependencies"
	@echo "test         Run tests"
	@echo "test-cov     Run tests with coverage report"
	@echo "lint         Run linter (flake8)"
	@echo "format       Format code (black)"
	@echo "type-check   Run type checker (mypy)"
	@echo "clean        Clean build artifacts"
	@echo ""

install:
	pip install -e .

install-dev:
	pip install -r requirements-dev.txt

test:
	pytest tests/ -v

test-cov:
	pytest tests/ --cov=ph --cov-report=html --cov-report=term-missing

lint:
	flake8 ph tests

format:
	black ph tests

type-check:
	mypy ph

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf htmlcov
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
.PHONY: help install install-venv install-dev test test-cov lint format type-check clean venv

help:
	@echo "Personal History - Development Commands"
	@echo ""
	@echo "install         Install package in development mode (requires pip)"
	@echo "install-venv    Create virtual environment and install package"
	@echo "install-dev     Install development dependencies"
	@echo "venv            Create virtual environment only"
	@echo "test            Run tests"
	@echo "test-cov        Run tests with coverage report"
	@echo "lint            Run linter (flake8)"
	@echo "format          Format code (black)"
	@echo "type-check      Run type checker (mypy)"
	@echo "clean           Clean build artifacts"
	@echo "clean-venv      Clean virtual environment"
	@echo ""

install:
	pip install -e .

install-venv:
	@echo "Creating virtual environment and installing package..."
	@python3 install.py --venv .venv

venv:
	@echo "Creating virtual environment..."
	@python3 -m venv .venv --prompt="personal-history"
	@echo "Virtual environment created at .venv"
	@echo "Activate with: source .venv/bin/activate (Linux/macOS) or .venv\\Scripts\\activate.bat (Windows)"

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

clean-venv:
	rm -rf .venv
	rm -f activate.sh
	rm -f activate.bat
	rm -f INSTALLATION_USAGE.md
.PHONY: run

install:
	pipenv install

install-dev:
	pipenv install --dev
	pipenv pre-comit install

test:
	pipenv run python -m unittest discover -s health_check/os/linux   -p "test_*.py"
	pipenv run python -m unittest discover -s health_check/os/windows -p "test_*.py"
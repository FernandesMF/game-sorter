lint:
	black .
	isort .
	flake8 .
	mypy .
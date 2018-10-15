
install-requirements:
	pip-sync boop/requirements.txt

update-requirements:
	pip-compile --upgrade --output-file boop/requirements.txt requirements.in

format:
	isort -y
	black .

test:
	pytest -vvv
	mypy --ignore-missing-imports --strict-optional boop
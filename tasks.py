from os import path

from invoke import task

SRC_DIR = path.dirname(__file__)


@task
def sync(c):
    c.run(f"pip-sync {SRC_DIR}/boop/requirements.txt")


@task
def update(c):
    c.run(
        f"pip-compile --upgrade --output-file {SRC_DIR}/boop/requirements.txt {SRC_DIR}/requirements.in"
    )


@task
def format(c):
    c.run(f"isort {SRC_DIR}")
    c.run(f"black {SRC_DIR}")


@task
def test(c):
    c.run(f"pytest {SRC_DIR} -vvv")
    c.run(f"mypy --ignore-missing-imports --strict-optional {SRC_DIR}/boop")


@task(pre=[sync])
def install(c):
    c.run(f"pip install -e {SRC_DIR}/boop/")
    
    
@task
def run(c):
    c.run(f"python {SRC_DIR}/boop/boop/main.py")

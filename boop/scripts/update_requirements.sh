#!/usr/bin/env bash
set -eE

function finish {
    echo CLEANING UP
    deactivate
    rm -rf env
}

function error {
    echo "FAILED!"
    finish
}

trap error ERR

echo CREATING ENV
python3.6 -m venv env
source env/bin/activate || exit 1
pip install -U pip

echo INSTALLING NEW REQUIREMENTS
pip install -U -r dev-requirements.txt

echo REPLACING OLD PINNED VERSIONS
pip freeze -r requirements.txt > requirements.txt
finish

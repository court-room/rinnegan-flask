#!/bin/bash

pipenv run black \
--check \
--config pyproject.toml \
.

pipenv run flake8 \
--config setup.cfg \
.

pipenv run isort \
--atomic \
--case-sensitive \
--check-only \
--force-alphabetical-sort-within-sections \
--force-single-line-imports \
--lines-after-imports 2 \
--lines-between-types 1 \
--line-width 79 \
--skip-glob "migrations/*" \
.

pipenv run pytest -c tests/pytest.ini

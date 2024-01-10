export PIPENV_VERBOSITY=-1
cd bot
pip install pipenv
pipenv install --dev --skip-lock
pipenv graph
echo "Running Python linting"
pipenv run mypy --version
pipenv run black --version
pipenv run isort --version
pylint --disable=C0116 --disable=C0114 --disable=R0401 --disable=W0613 --disable=W0718 --disable=C0115 support_bot
flake8 --show-source --statistics --max-complexity 6 support_bot tests
echo "Running autoflake on support_bot and tests files"
pipenv run autoflake --recursive --check --ignore-init-module-imports --remove-unused-variables --remove-all-unused-imports support_bot tests
echo "Running mypy, black, and isort checks"
pipenv run mypy .
pipenv run black --check support_bot tests
pipenv run isort --check-only support_bot tests
echo "Python linting completed successfully"
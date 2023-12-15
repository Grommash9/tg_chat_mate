mypy --version
black --version
flake8 --version
isort --version
pip-audit --version
bandit --version
autoflake --version

find support_bot/ -name "*.py" -exec autoflake --in-place --remove-unused-variables --remove-all-unused-imports {} \;
find tests/ -name "*.py" -exec autoflake --in-place --remove-unused-variables --remove-all-unused-imports {} \;

mypy .

black --check support_bot tests
isort --check-only .
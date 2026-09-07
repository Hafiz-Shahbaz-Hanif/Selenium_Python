.PHONY: install test smoke parallel allure allure-serve categories lint clean

install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

# Drop the defect-classification rules where Allure expects them, before a run.
categories:
	mkdir -p reports/allure-results
	cp allure/categories.json reports/allure-results/categories.json

# Full suite, sequential, with Allure results
test: categories
	behave -f allure_behave.formatter:AllureFormatter -o reports/allure-results -f pretty

# Only @smoke scenarios
smoke: categories
	behave --tags=@smoke -f allure_behave.formatter:AllureFormatter -o reports/allure-results -f pretty

# Parallel execution via behavex (feature-level workers)
parallel:
	behavex -o reports/behavex --parallel-processes 4 --parallel-scheme feature

# Build + open the Allure HTML report
allure: categories
	allure generate reports/allure-results --clean -o reports/allure-report

allure-serve: categories
	allure serve reports/allure-results

lint:
	flake8 .

clean:
	rm -rf reports allure-results allure-report **/__pycache__

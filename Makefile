.PHONY: install test smoke parallel allure allure-serve lint clean

install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

# Full suite, sequential, with Allure results
test:
	behave -f allure_behave.formatter:AllureFormatter -o reports/allure-results -f pretty

# Only @smoke scenarios
smoke:
	behave --tags=@smoke -f allure_behave.formatter:AllureFormatter -o reports/allure-results -f pretty

# Parallel execution via behavex (feature-level workers)
parallel:
	behavex -o reports/behavex --parallel-processes 4 --parallel-scheme feature

# Build + open the Allure HTML report
allure:
	allure generate reports/allure-results --clean -o reports/allure-report

allure-serve:
	allure serve reports/allure-results

lint:
	flake8 .

clean:
	rm -rf reports allure-results allure-report **/__pycache__

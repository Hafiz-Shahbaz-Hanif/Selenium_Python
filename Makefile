.PHONY: install test smoke parallel allure allure-serve categories lint clean

install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

# Seed Allure metadata (defect categories + run environment) before a run.
categories:
	mkdir -p reports/allure-results
	cp allure/categories.json reports/allure-results/categories.json
	printf '%s\n' \
		'Framework=Selenium 4 + Behave + Page Object Model' \
		'Runner=behave (behavex for parallel, feature-level workers)' \
		'Browser=chrome / firefox (Selenium Manager, no driver binaries)' \
		'UI.SauceDemo=https://www.saucedemo.com' \
		'UI.OrangeHRM=https://opensource-demo.orangehrmlive.com' \
		> reports/allure-results/environment.properties

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

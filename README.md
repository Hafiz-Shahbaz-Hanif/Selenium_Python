# Selenium + Python + Behave — BDD Web Automation Framework

[![CI](https://github.com/Hafiz-Shahbaz-Hanif/Selenium_Python/actions/workflows/ci.yml/badge.svg)](https://github.com/Hafiz-Shahbaz-Hanif/Selenium_Python/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-4.x-43B02A?logo=selenium&logoColor=white)
![Behave](https://img.shields.io/badge/BDD-Behave%2FGherkin-23D96C?logo=cucumber&logoColor=white)
![Allure](https://img.shields.io/badge/Report-Allure-FF7043)
![License](https://img.shields.io/badge/license-MIT-blue)

A behaviour-driven web automation framework built with **Selenium WebDriver**, **Python** and
**Behave**, on a strict **Page Object Model**, with **Allure** reporting, failure screenshots
and parallel execution.

| | |
|---|---|
| **Applications under test** | [SauceDemo](https://www.saucedemo.com) · [OrangeHRM (open-source demo)](https://opensource-demo.orangehrmlive.com) |
| **BDD** | Behave (Gherkin `.feature` files + Python step definitions) |
| **Driver management** | Selenium Manager — **no driver binaries** to install or commit |
| **Reporting** | Allure + JUnit XML + `behave.log` |
| **Parallel** | `behavex` (feature-level workers) |
| **CI** | GitHub Actions (headless Chrome) |

---

## Highlights

- **Strict Page Object Model** — `BasePage` centralises waits, safe clicks
  (scroll-into-view + JS-click fallback) and navigation; step definitions never
  touch a locator or the raw driver.
- **Stable against SPA quirks** — `click_and_wait_for_url()` retries clicks that
  land before a React page has hydrated, instead of sleeping.
- **Two applications** — SauceDemo (login, catalogue sorting, cart, full checkout)
  and OrangeHRM (a slower app, different locator strategies) to show the framework
  is not coupled to one site.
- **Data-driven** — `Scenario Outline` for login permutations and sort orders;
  a custom Behave type so quoted values may be empty.
- **Failure triage built in** — on any failed step the screenshot, URL and page
  source are attached to the Allure report (`features/environment.py`).
- **Config as code** — `config/config.py` is a typed, frozen dataclass driven by
  environment variables and Behave `-D` userdata, with working defaults.
- **Data-driven at scale** — ~110 scenarios, most as `Scenario Outline` tables
  (all 6 products × add / remove / detail / buy; every main OrangeHRM module).
- **Developed with an agentic-AI workflow** — `CLAUDE.md` plus `.claude/` subagents
  (`failure-triager`, `page-object-author`) and skills (`new-bdd-scenario`,
  `allure-triage`).

## Coverage

| Feature | Scenarios | Notes |
|---|---|---|
| `login` | 12 | 5 user types reach the catalogue, bad-input outline, sign-out |
| `inventory` | 25 | sort (4), add / add-remove / shelf-price per product (6 each) |
| `product` | 14 | detail name/price/description and add-to-cart per product |
| `cart` | 16 | listed / removed per product, prices match catalogue |
| `checkout` | 14 | buy each product with 8% tax + total maths, field validation, cancels |
| `orangehrm_login` | 2 | valid / invalid |
| `orangehrm_navigation` | 25 | open + presence for all 12 main-menu modules, logout |

## Project structure

```
.
├── CLAUDE.md                  # conventions for AI agents working in this repo
├── .claude/
│   ├── agents/                # failure-triager, page-object-author
│   └── skills/                # new-bdd-scenario, allure-triage
├── features/
│   ├── environment.py        # Behave hooks: driver lifecycle, failure artifacts
│   ├── *.feature             # Gherkin specs
│   └── steps/                # step definitions (one module per area)
├── pages/                    # Page Object Model (BasePage + one class per screen)
├── utils/                     # driver_factory, products catalogue data
├── config/config.py          # typed configuration
├── behave.ini                # Behave + userdata defaults
├── Makefile                  # install / test / smoke / parallel / allure
└── .github/workflows/ci.yml  # SauceDemo (gating) + OrangeHRM (non-blocking) jobs
```

## Getting started

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # optional — defaults already target the public demos
```

## Running

```bash
behave                                   # full suite (headless)
behave --tags=@smoke                     # smoke only
behave --tags=@saucedemo                 # one application
behave -D headless=false -D browser=firefox   # headed Firefox
make parallel                            # behavex, 4 workers, feature-level
```

Behave userdata (`-D`): `headless` (true/false), `browser` (chrome/firefox).

## Reports

```bash
make test           # run with Allure results in reports/allure-results
make allure         # build reports/allure-report
make allure-serve   # serve it
```

## CI

`.github/workflows/ci.yml` installs Chrome, runs the headless BDD suite on every push
and PR, and uploads `allure-results`, JUnit XML and the run log as artifacts.

---

## Author

**Hafiz Shahbaz Hanif** — Staff SQA Engineer / Test Automation Architect
[LinkedIn](https://www.linkedin.com/in/hafiz-shahbaz-hanif-70407417a) · [GitHub](https://github.com/Hafiz-Shahbaz-Hanif)

Licensed under the [MIT License](LICENSE).

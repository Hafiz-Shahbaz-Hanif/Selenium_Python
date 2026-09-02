# CLAUDE.md — working agreement for AI agents in this repo

This BDD framework is developed with an **agentic-AI workflow**: Claude Code and the
subagents/skills in `.claude/` draft scenarios and page objects, triage failures, and
review diffs against the conventions below.

## What this project is

| | |
|---|---|
| Apps under test | [SauceDemo](https://www.saucedemo.com) · [OrangeHRM demo](https://opensource-demo.orangehrmlive.com) |
| Runner / BDD | Behave (Gherkin `.feature` + Python steps) |
| Design | Page Object Model (`pages/`, `BasePage` + one class per screen) |
| Driver | Selenium 4 + Selenium Manager — **no driver binaries** |
| Reporting | Allure (`allure-behave`) + JUnit + failure screenshots |
| Parallel | `behavex` (feature-level workers) |

## Golden rules

1. **Behaviour in `.feature` files.** Prefer `Scenario Outline` + `Examples` for data
   variations — each row is one real test case.
2. **Page Object Model, strictly.** Step definitions never touch a locator, a
   `WebDriverWait`, `driver.*`, or `expect`. They call an intent-revealing page method
   and assert with `hamcrest` (`assert_that(...)`).
3. **Locators only in page classes**, as `(By.CSS_SELECTOR, '[data-test="..."]')`
   class constants. `data-test` first; XPath only when there is no test id (OrangeHRM).
4. **No `time.sleep`.** Use `BasePage` waits: `find`, `is_visible(timeout=...)`,
   `wait_for_url_contains`, `wait_for_dom_ready`, `click_and_wait_for_url`.
5. **SauceDemo is React** — a click before hydration is dropped. Navigation clicks go
   through `click_and_wait_for_url(...)`, which retries.
6. **Determinism.** `before_scenario` gives every scenario a fresh browser. Scenarios
   own their state (add their own cart items) and must pass in any order / in parallel.
7. **Config via `config/config.py`** — env vars + Behave `-D` userdata, working defaults.
   No URLs/credentials as literals in steps or pages.
8. **Failure artifacts** are attached to Allure by `features/environment.py` — don't
   re-implement screenshotting in steps.

## Layout

```
features/*.feature            Gherkin
features/steps/*_steps.py      step definitions (thin; shared registry)
features/environment.py        hooks: driver lifecycle, failure screenshots
pages/*.py                     Page Object Model
utils/driver_factory.py        Chrome/Firefox/Remote WebDriver
config/config.py               typed config
```

## Commands

```bash
behave                                    # full suite (headless)
behave --tags=@smoke
behave --tags=@saucedemo
behave -D headless=false -D browser=firefox
make parallel                             # behavex, 4 workers
make test && make allure                  # Allure results + HTML report
flake8 .
```

## Definition of done

- `flake8 .` clean
- The affected `--tags` run green (note any external-demo flakiness)
- New behaviour is Gherkin; new steps are one page call + one `assert_that`
- Tags: `@saucedemo`/`@orangehrm`, plus `@smoke` for one happy path per area
- Data variations added as `Examples` rows, not copied scenarios

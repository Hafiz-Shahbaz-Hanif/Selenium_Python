# Contributing

Thanks for looking at this project. It is a portfolio framework, but it is built
to real standards and PRs are welcome.

## Ground rules

The conventions in [`CLAUDE.md`](CLAUDE.md) are the contract — read it first. In
short:

- **Behaviour in `.feature` files.** Prefer `Scenario Outline` + `Examples` for
  data variations — each row is one real test case.
- **Page Object Model, strictly.** No locator, `WebDriverWait`, `driver.*` or
  assertion in a step; steps call a page method and `assert_that(...)`.
- **Locators only in page classes**, as `(By.CSS_SELECTOR, '[data-test="..."]')`
  constants. `data-test` first; XPath only where there is no test id.
- **No `time.sleep`** — use the `BasePage` waits.
- **SauceDemo is React** — navigation clicks go through
  `click_and_wait_for_url(...)`.

## Getting set up

```bash
python -m venv .venv && .venv\Scripts\activate      # or source .venv/bin/activate
pip install -r requirements.txt
behave --tags=@smoke
```

## Adding a scenario

1. Add or extend a `.feature`. Data variations go in an `Examples` table, not
   copied scenarios.
2. Reuse existing step text (`grep features/steps/`). New steps are **one page
   call + one `assert_that`**.
3. New screen → a new class under `pages/` extending `BasePage`; new locators are
   class constants on that page.
4. Tag it: `@saucedemo` / `@orangehrm`, plus `@smoke` for one happy path per area.

## Before you open a PR

```bash
flake8 .
behave --tags=@<affected>          # note any public-demo flakiness in the PR
make parallel                      # optional: behavex, 4 workers
```

- [ ] `flake8 .` clean
- [ ] New behaviour is Gherkin; steps stay thin
- [ ] No `time.sleep`; failure artefacts still handled by `environment.py`
- [ ] Data variations are `Examples` rows
- [ ] Commit messages are conventional (`feat(pages): …`, `test: …`, `docs: …`)

## AI-assisted workflow

`.claude/` contains the subagents and skills used to develop this repo
(`failure-triager`, `page-object-author`, and the `new-bdd-scenario` /
`allure-triage` skills). They encode the same rules as this document.

---
name: new-bdd-scenario
description: Scaffold a new Gherkin scenario or feature for this Behave + Selenium + POM framework, wired to existing (or new, thin) step definitions and page objects.
---

# Add a BDD scenario

## 1. Pick the file and tags

- SauceDemo → `features/<area>.feature`, tag `@saucedemo`
- OrangeHRM → `features/orangehrm_<area>.feature`, tag `@orangehrm`
- One `@smoke` per area (a single happy path). `@e2e` for full journeys.

## 2. Write it as behaviour

- One capability per `Feature`; `Background` for shared setup
  (`Given I am signed in to SauceDemo as the standard user`).
- Prefer a `Scenario Outline` with an `Examples` table for variations. Leave a cell
  blank for an empty value (the `Optional` parse type handles `""`).
- Steps are sentences, not clicks: `When I add "Sauce Labs Backpack" to the cart`.

## 3. Reuse steps

Search `features/steps/` for a matching step first. A new step is **one page-object
call + one `assert_that(...)`** — nothing else. Register capture groups in order.

## 4. New page behaviour

Add an action/query to the relevant `pages/*.py`. If a whole screen is missing, use
the `page-object-author` agent.

## 5. Verify

```bash
flake8 .
behave --tags=@<your-tag> -D headless=true
```

Confirm a failure attaches a screenshot to `reports/allure-results/`.

## Checklist

- [ ] Scenario is independent (adds its own cart items, no ordering assumption)
- [ ] No locator / wait / `driver` / `WebDriverWait` in the step file
- [ ] No `time.sleep`
- [ ] `flake8` clean; targeted run green

---
name: allure-triage
description: Turn a reports/allure-results folder into a ranked failure summary for this Behave framework — grouping by root cause and pulling the failure screenshot, URL and page source for each failed scenario.
---

# Triage an Allure run

## 1. Locate results

```bash
make allure        # builds reports/allure-report from reports/allure-results
```

Raw material: `reports/allure-results/*-result.json` (one per scenario) and the
attachments (`screenshot`, `url`, `page source`) written by `features/environment.py`
on failure. `reports/behave.log` and `reports/junit/*.xml` add timing/context.

## 2. Failure table

For each `*-result.json` with `status` = `failed` / `broken`:

| field | source |
|---|---|
| scenario | `name` / `fullName` |
| tags | `labels[]` (`name == "tag"`) |
| failed step | last non-passed entry in `steps[]` |
| message | `statusDetails.message` (first line) |
| url at failure | the attached `url` text |
| screenshot | the attached PNG |

## 3. Group by cause

Cluster failures with a shared message or page class. Common clusters:
React-hydration (dropped nav click), locator drift (one `data-test`/XPath),
OrangeHRM demo reset, SauceDemo account lockout, demo-app slowness (long durations).

## 4. Rank

1. Real product bugs (deterministic wrong value)
2. Framework defects hitting many scenarios (one page/step)
3. Single flaky scenario
4. External (demo down/slow)

## Output

Ranked clusters → scenarios affected → cause → fix owner, plus the one command to
reproduce the top item (`behave features/<file>:<line>`). Hand fixes to
`failure-triager`.

# Changelog

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## 2026-09-24

### Fixed
- README coverage numbers had drifted: `orangehrm_navigation` was listed as 25
  scenarios (actual: 23 — 1 landing + 9-row menu-opens outline + 12-row
  availability outline + 1 logout), and the total was ~110 instead of the
  actual ~106. Recounted directly from every `.feature` file.

## 2026-09-23

### Changed
- Split `requirements.txt` into runtime-only deps and a new `requirements-dev.txt`
  (adds `flake8`, `pre-commit`) — a plain install no longer pulls dev tooling.

## 2026-09-22

### Added
- Cancel superseded CI runs on the same branch (`concurrency` group in the workflow).

## 2026-09-19

### Added
- `.pre-commit-config.yaml` (flake8 + trailing-whitespace / EOF / YAML / merge-conflict hooks).

## 2026-09-16

### Added
- Dependabot for `pip` and `github-actions`.

## 2026-09-13

### Added
- `SECURITY.md` (absolute-URL issues link).

## 2026-09-11

### Added
- `docs/TAGS.md`: tag reference and `behave.ini` userdata examples.

## 2026-09-08

### Added
- `make categories` also seeds Allure `environment.properties`; README section on
  `behavex` parallel runs.

## 2026-09-07

### Added
- Allure defect-classification `allure/categories.json`, wired into `make` and CI.

## 2026-09-06

### Added
- `.github/ISSUE_TEMPLATE/{bug_report,flaky_test}.md`, `.github/pull_request_template.md`.

## 2026-09-05

### Added
- `.editorconfig` mirroring the flake8 config in `setup.cfg`.

## 2026-09-03

### Added
- `CONTRIBUTING.md` (Behave/POM rules, setup, PR checklist).

## 2026-09-02

### Added
- `.claude/` AI-assisted workflow: `failure-triager`, `page-object-author`
  subagents; `new-bdd-scenario`, `allure-triage` skills; `CLAUDE.md`.
- SauceDemo coverage: user-type login matrix and sign-out, per-product catalogue,
  product detail, cart and checkout (8% tax / total maths, validation, cancels).
- OrangeHRM: dashboard page object and main-menu navigation across every module.
- CI split into a gating SauceDemo job and a non-blocking OrangeHRM job.

### Fixed
- Synthetic-click fallback for React routing buttons on headless Chrome 152.
- Orphaned browser processes are reaped after each scenario (`psutil`).

## 2026-08-31

### Added
- Initial scaffold: Selenium + Python + Behave (BDD), typed config, Selenium
  Manager driver factory (chrome/firefox/remote), Page Object Model for SauceDemo,
  login/sorting/cart/checkout scenarios with failure screenshots, OrangeHRM login,
  Makefile, `.env` example, CI with Allure artifacts, README.

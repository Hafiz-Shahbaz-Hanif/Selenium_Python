<!-- See CONTRIBUTING.md and CLAUDE.md for the full conventions. -->

## What & why

<!-- One or two lines. Link the issue if there is one. -->

## Checklist

- [ ] `flake8 .` clean
- [ ] The affected `--tags` run green (note any external-demo flakiness)
- [ ] New behaviour is Gherkin; new steps are one page call + one `assert_that`
- [ ] Locators live only in page classes, `data-test` first
- [ ] No `time.sleep`; failure artefacts still handled by `environment.py`
- [ ] Data variations are `Examples` rows, not copied scenarios
- [ ] Tags applied (`@saucedemo` / `@orangehrm`, plus `@smoke` for one happy path)

## Notes for the reviewer

<!-- Anything non-obvious: a demo quirk worked around, a deliberate deviation, follow-ups. -->

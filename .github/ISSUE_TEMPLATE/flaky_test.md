---
name: Flaky test
about: A scenario that passes on rerun without a code change
title: "[flaky] "
labels: flaky
---

## Which scenario

<!-- feature : scenario (or Scenario Outline + Examples row) -->

## Evidence it is flaky

- [ ] Passed on rerun with no code change
- [ ] Fails only in parallel (`behavex`) / only in CI / only headless
- Rough failure rate: __ / 10 runs

## Failure detail

<!-- The assertion or WebDriver exception, and the step it happened on. -->

## Suspected cause

<!-- missing BasePage wait, SauceDemo React hydration, OrangeHRM slow reset,
     shared state between scenarios, animation. -->

## Notes

Link the CI run and the screenshot. The `failure-triager` agent in `.claude/` is
built for this.

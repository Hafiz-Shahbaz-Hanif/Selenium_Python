# Tags and userdata

## Gherkin tags

Every feature carries an application tag plus one or more area tags; the
happy-path scenario in each feature also carries `@smoke`.

| Tag | Meaning |
|---|---|
| `@saucedemo` | Runs against saucedemo.com |
| `@orangehrm` | Runs against the OrangeHRM demo |
| `@login` | Authentication (either app) |
| `@cart` | SauceDemo shopping cart |
| `@checkout` | SauceDemo checkout flow |
| `@inventory` | SauceDemo product catalogue |
| `@product` | SauceDemo product detail page |
| `@navigation` | OrangeHRM main-menu navigation |
| `@e2e` | A full multi-step journey (e.g. checkout end to end) |
| `@smoke` | One happy path per feature — the fast, must-pass subset |

Combine tags with `and`/`or`/`not`:

```bash
behave --tags=@smoke                        # smoke only, both apps
behave --tags=@saucedemo                    # everything on SauceDemo
behave --tags="@saucedemo and @smoke"       # SauceDemo smoke only
behave --tags="@cart or @checkout"          # cart and checkout, skip the rest
behave --tags="@saucedemo and not @e2e"     # SauceDemo, skip the long journeys
```

## `behave.ini` userdata

`[behave.userdata]` in `behave.ini` sets the defaults; override any key per run
with `-D`:

```bash
behave -D headless=false                    # watch it run
behave -D browser=firefox                   # Firefox instead of Chrome
behave -D headless=false -D browser=firefox --tags=@login
```

`config/config.py` reads these the same way it reads environment variables and
`.env` — see `CLAUDE.md` for the full resolution order.

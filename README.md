# Bolig Ping

Get a ping when your dream home in Denmark becomes available on Boligsiden.dk.

______________________________________________________________________
[![Code Coverage](https://img.shields.io/badge/Coverage-89%25-yellowgreen.svg)](https://github.com/saattrupdan/bolig-ping/tree/main/tests)
[![Documentation](https://img.shields.io/badge/docs-passing-green)](https://saattrupdan.github.io/bolig-ping)
[![License](https://img.shields.io/github/license/saattrupdan/bolig-ping)](https://github.com/saattrupdan/bolig-ping/blob/main/LICENSE)
[![LastCommit](https://img.shields.io/github/last-commit/saattrupdan/bolig-ping)](https://github.com/saattrupdan/bolig-ping/commits/main)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.0-4baaaa.svg)](https://github.com/saattrupdan/bolig-ping/blob/main/CODE_OF_CONDUCT.md)

Developer:

- Dan Saattrup Nielsen (saattrupdan@gmail.com)


## Quickstart

The easiest way to use the package is as a
[uv](https://docs.astral.sh/uv/getting-started/installation/) tool. You can simply start
searching for properties using the following command:

```bash
uvx bolig-ping --city københavn
```

This both installs the package and runs the command. All the available options are
listed below, but you can always get these by running the following command:

```bash
uvx bolig-ping --help
```


To be able to send emails, you have to create a [Google app
password](https://myaccount.google.com/apppasswords), and store both your Gmail email
address and the app password in the environment variables `GMAIL_EMAIL` and
`GMAIL_PASSWORD`, respectively. You can also simply store these in a `.env` file, as
follows:

```bash
GMAIL_EMAIL=<your-email>@gmail.com
GMAIL_PASSWORD=<your-app-password>
```

With this set up, you can now use the `--email` option to receive an email with new
properties that match your search criteria:

```bash
uvx bolig-ping --city københavn --email <receiving-email>
```

This will then send an email from your `GMAIL_EMAIL` to the `receiving-email` address.
You can also set up a recurring search if you have a server available. In this case, you
can add the following line to your [crontab](https://linuxhandbook.com/crontab/) on a
server, to run the search every hour:

```bash
0 * * * * <uvx-full-path> bolig-ping <search-arguments>
```

Here `<uvx-full-path>` is the full path to the `uvx` command, which you can find by
running `which uvx` in your terminal.


## All options

The following options are available:

- `--city/-c`: The city you want to search in. This argument can be used several times
  to search in multiple cities, e.g., `-c aarhus -c odense`. If you do not specify any
  city then you'll be searching for homes in _all_ of Denmark!
- `--min-price`: The minimum price of the property, in DKK. Default is no minimum price.
- `--max-price`: The maximum price of the property, in DKK. Default is no maximum price.
- `--min-monthly-fee`: The minimum monthly fee of the property, in DKK. Default is no
  minimum monthly fee.
- `--max-monthly-fee`: The maximum monthly fee of the property, in DKK. Default is no
  maximum monthly fee.
- `--min-rooms`: The minimum number of rooms in the property. Default is no minimum
  number of rooms.
- `--max-rooms`: The maximum number of rooms in the property. Default is no maximum
  number of rooms.
- `--min-size`: The minimum size of the property, in square meters. Default is no
  minimum size.
- `--max-size`: The maximum size of the property, in square meters. Default is no
  maximum size.
- `--query/-q`: The query to search for in the property description. This argument can
  be used several times to search for multiple queries, e.g., `-q badekar -q altan`.
- `--property-type/-t`: The type of property to search for. The available property
  types are `ejerlejlighed`, `andelslejlighed` and `house`. This argument can be used
  several times to search for multiple property types, e.g., `-t ejerlejlighed -t house`.
  Default is searching for all property types.
- `--email`: The email address you want to receive the ping on. Note that this needs to
  have the `GMAIL_EMAIL` and `GMAIL_PASSWORD` environment variables set, as described
  above. Default is to use no email address, and instead print the properties to the
  console.
- `--cache/--no-cache`: Whether to use the cache or not. Default is to use the cache,
  but you can disable it by using the `--no-cache` flag. This is useful if you want to
  see all the results, and not just the new ones. The cache is stored in the
  `.boligping_cache` file in the current directory.
- `--headless/--no-headless`: Whether to run the scraper in headless mode. Mostly used
  for debugging.

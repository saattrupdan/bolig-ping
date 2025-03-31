# Bolig Ping

Get a ping when your dream flat in Denmark becomes available on Boligsiden.dk.

______________________________________________________________________
[![Code Coverage](https://img.shields.io/badge/Coverage-75%25-yellowgreen.svg)](https://github.com/saattrupdan/bolig-ping/tree/main/tests)
[![Documentation](https://img.shields.io/badge/docs-passing-green)](https://saattrupdan.github.io/bolig-ping)
[![License](https://img.shields.io/github/license/saattrupdan/bolig_ping)](https://github.com/saattrupdan/bolig-ping/blob/main/LICENSE)
[![LastCommit](https://img.shields.io/github/last-commit/saattrupdan/bolig_ping)](https://github.com/saattrupdan/bolig-ping/commits/main)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.0-4baaaa.svg)](https://github.com/saattrupdan/bolig-ping/blob/main/CODE_OF_CONDUCT.md)

Developer:

- Dan Saattrup Nielsen (saattrupdan@gmail.com)


# Quickstart

The easiest way to use the package is as a `uv` tool. You can simply start searching for
flats using the following command:

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


# All options

The following options are available:

- `--city/-c` (required): The city you want to search in. This argument can be
  used several times to search in multiple cities, e.g., `-c aarhus -c odense`.
- `--min-price`: The minimum price of the flat, in DKK. Default is no minimum price.
- `--max-price`: The maximum price of the flat, in DKK. Default is no maximum price.
- `--min-rooms`: The minimum number of rooms in the flat. Default is no minimum number
  of rooms.
- `--max-rooms`: The maximum number of rooms in the flat. Default is no maximum number
  of rooms.
- `--min-size`: The minimum size of the flat, in square meters. Default is no minimum
  size.
- `--max-size`: The maximum size of the flat, in square meters. Default is no maximum
  size.
- `--email`: The email address you want to receive the ping on. Note that this needs to
  have the `GMAIL_EMAIL` and `GMAIL_PASSWORD` environment variables set, as described
  above. Default is to use no email address, and instead print the flats to the
  console.

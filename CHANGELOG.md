# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).


## [Unreleased]



## [v1.6.0] - 2025-04-24
### Added
- Now allows multiple emails with the `--email` (`-e`) argument.

### Changed
- We now use the Boligsiden API instead of scraping the website. This makes the
  application much faster and more reliable, as we no longer have to deal with
  changes to the website layout. It also puts less load on the Boligsiden servers.
- The cache has been renamed to `.bolig_ping_cache` from `.boligping_cache`. To ensure
  that this is backwards compatible, we will rename `.boligping_cache` to
  `.bolig_ping_cache` if the former exists and not the latter.


## [v1.5.0] - 2025-04-23
### Added
- Check whether the `GMAIL_EMAIL` and `GMAIL_PASSWORD` environment variables are set
  before doing anything.

### Fixed
- Optimised the caching, which now ensures that we do not have to check a property
  listing twice. This was not always the case, as we only cached the ones that were sent
  to the given email, and not the ones that were filtered out.


## [v1.4.0] - 2025-04-20
### Added
- Added `--headless/--no-headless` flag, which is mostly used for debugging.

### Changed
- No requirement of the `--city` argument now; it defaults to all cities in Denmark.
- All arguments now defaults to None, meaning that the default behaviour of
  Boligsiden.dk is used, which currently is exactly the same as the previous behaviour.

### Fixed
- Better detection of when the inputted city name is invalid.


## [v1.3.0] - 2025-04-19
### Added
- Added the ability to search for different property types, with the new
  `--property-type` (`-t`) option. The available property types are `ejerlejlighed`,
  `andelslejlighed` and `house`. You can specify multiple property types with, e.g.,
  `bolig-ping <other-arguments> -t ejerlejlighed -t house`. It defaults to
  `ejerlejlighed`, which is the only type that was previously supported.
- Added new `--min-monthly-fee` and `--max-monthly-fee` options to filter flats by
  monthly fee. The default is no minimum or maximum monthly fee.
- Added new `--cache/--no-cache` flag, which allows you to disable the cache. The
  default behaviour is still to use the cache, but you can disable it by using the
  `--no-cache` flag. This is useful if you want to see all the results, and not just the
  new ones. The cache is stored in the `.boligping_cache` file in the current directory.

### Changed
- Changed the `--query` (`-q`) option to now search for the selected keywords in the
  description of the flat, rather than use Boligsiden.dk's own keywords, since many
  flats do not use these keywords. Remember that you can specify multiple queries with,
  e.g., `bolig-ping <other-arguments> -q badekar -q altan`.

### Fixed
- Now catches when an invalid city name is provided, and returns a helpful error
  message. Previously, it would just print the raw traceback.


## [v1.2.0] - 2025-04-04
### Added
- Added CLI command aliases `bolig-ping` and `boligping`.


## [v1.1.0] - 2025-03-31
### Added
- Added support for `--max-rooms` and `--max-size`.


## [v1.0.0] - 2025-03-30
### Added
- Initial version of the project, featuring the ability to fetch data on new flats
  (ejerlejligheder) from Boligsiden.dk, and sending email notifications when new
  flats are found.

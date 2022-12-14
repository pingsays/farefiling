# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2022-07-30

### Added

- Functionality to split output into Business Class fares vs Non-Business Class fares
- More logging to help with debugging
- Functionality to choose to use Excel config instead of toml as it is more user friendly
- A utility function (\_setup_logger) to add the function's name to the logger's name to improve logging

### Changed

- Application config from hardcoded variables in app.py to a config file (config.toml)

## [0.2.1] - 2022-07-29

### Added

- Logging of the data types of the Dataframes for DEBUG level

## [0.2.0] - 2022-07-29

### Added

- A config file (config.toml) to manage application config
- Logger to utilities module
- 'output.xlsx' to .gitignore

### Changed

- Refactored gen_fare_combination function in utilities module to a more pythonic way of unpacking Excel data into variables

## [0.1.0] - 2022-07-29

### Added

- New farefiling app that is refactored from [github.com/pingsays/pingsays](https://github.com/pingsays/pingsays)

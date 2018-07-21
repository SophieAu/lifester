# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

Possible change tags are: ``Added``, ``Changed``, ``Deprecated``, ``Removed``, ``Fixed``, ``Security``


## [Unreleased]
### Added
- When hitting a fatal parsing error, lifester now quits (more) gracefully
- Analytics now include total hours awake

## Fixed
- Parser would duplicate last entry of the day instead of adding a sleep entry
- Parser will no longer add a sleep entry when going bed at exactly midnight
- Fatal bug when two lines followed each other
- Formatting in analytics output
- Empty lines were recognized as categories


## [1.1.0] - 2018-07-16
### Added
- Analytics include new value: average hours of sleep over timeframe
- File parsing works for my custom format (instead of manually entering vie `lifester enter`)

## Fixed
- Sleep block at the end of the day was not being added to json file
- Timeframe parsing did not adhere to documentation

## Removed
- Percentage of time tracked from analytics to due bringing no value


## 1.0.0 - 2018-07-13
### Added
- Entering data via cli interface
- Analyzing data on a yearly, monthly, or weekly basis
- Analyzing all entered data
- Adding categories


[Unreleased]: https://github.com/sophieau/lifester/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/sophieau/lifester/compare/v1.0...v1.1.0

# Changelog

All notable changes to MicTest12-1.0 will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Table of Contents

- [Unreleased](#unreleased)
- [Version 1.0.0](#100---2026-05-01)
- [Version 0.9.0](#090---2026-04-15)
- [Version 0.8.0](#080---2026-03-20)
- [Version 0.7.0](#070---2026-02-10)
- [Earlier Versions](#earlier-versions)

## [Unreleased]

### Added

- Comprehensive markdown documentation suite
- Developer onboarding guide
- API reference documentation
- Contributing guidelines

### Changed

- Updated README with detailed project information
- Improved project structure documentation

### Deprecated

- Legacy testing utilities (will be removed in 2.0.0)

## [1.0.0] - 2026-05-01

### Added

- **Core Features**
  - Initial stable release
  - Full test runner implementation
  - Comprehensive assertion library
  - Mocking and spying capabilities

- **Testing Capabilities**
  - Unit testing framework
  - Integration testing support
  - End-to-end test runner
  - Snapshot testing

- **Developer Tools**
  - CLI for running tests
  - Watch mode for development
  - Coverage reporting
  - Multiple output formats

### Fixed

- Race condition in async test execution
- Memory leak in long-running test suites
- Test isolation issues with shared state

### Security

- Updated dependencies to latest secure versions
- Improved input sanitization
- Added security audit to CI pipeline

## [0.9.0] - 2026-04-15

### Added

- **New Features**
  - Parallel test execution
  - Custom test reporters
  - Plugin architecture
  - Configuration validation

- **Improvements**
  - Better error messages
  - Improved performance metrics
  - Enhanced debugging output

### Changed

- Migrated from CommonJS to ESM modules
- Updated minimum Node.js version to 16.x
- Restructured internal API

### Removed

- Deprecated `oldTestRunner` API
- Legacy callback-based assertions
- Outdated configuration options

## [0.8.0] - 2026-03-20

### Added

- **TypeScript Support**
  - Type definitions for all APIs
  - TypeScript test examples
  - Strict mode compatibility

- **Testing Features**
  - Async/await support in all assertions
  - Custom matcher creation
  - Test fixture management

### Fixed

- Issue with Windows path separators
- Bug in regex matching
- Memory issues with large test suites

## [0.7.0] - 2026-02-10

### Added

- **Initial Beta Features**
  - Basic test runner
  - Core assertion library
  - Simple mocking support
  - Configuration file support

- **Documentation**
  - Initial README
  - Basic usage examples
  - API documentation skeleton

### Changed

- Improved CLI argument parsing
- Better default configurations
- Updated dependencies

## Earlier Versions

### [0.6.0] - 2026-01-15

- Alpha release with experimental features
- Initial test runner prototype
- Basic assertions

### [0.5.0] - 2025-12-20

- Pre-alpha development version
- Internal testing only
- Foundation work

## Migration Guides

### Migrating from 0.x to 1.0

Major changes when upgrading:

- **API Changes**
  - Replace `oldRunner()` with `runner()`
  - Update import statements to use ESM
  - Remove deprecated callback patterns

- **Configuration Changes**
  - Move config from `package.json` to dedicated file
  - Update path references to use new format
  - Refactor custom matchers

- **Breaking Changes**
  - Minimum Node.js version is now 16.x
  - Removed support for synchronous tests
  - Changed default timeout values

### Migrating from 0.8 to 0.9

Key updates:

- Switch to ESM imports
- Update Node.js to version 16+
- Replace removed APIs

## Versioning Policy

We follow Semantic Versioning:

- **MAJOR** version: Incompatible API changes
- **MINOR** version: New backwards-compatible functionality
- **PATCH** version: Backwards-compatible bug fixes

## Release Schedule

Our release cadence:

- **Patch releases**: As needed for critical bugs
- **Minor releases**: Monthly for new features
- **Major releases**: Yearly with deprecation notices
- **Security releases**: Immediate when needed

## Contributing to the Changelog

When contributing changes:

- Add entries under `[Unreleased]` section
- Use clear, descriptive language
- Group changes by category (Added, Changed, etc.)
- Reference issue/PR numbers when applicable
- Follow existing formatting patterns

## Categories Reference

Each release uses these categories:

- **Added**: New features
- **Changed**: Changes to existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Now removed features
- **Fixed**: Bug fixes
- **Security**: Vulnerability fixes

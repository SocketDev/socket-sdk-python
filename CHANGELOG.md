# Changelog

## 3.5.0

### Changed: bound runtime dependency ranges and pin build backend

- Added version bounds to the runtime dependencies: `requests>=2.32.5,<3`
  (previously unbounded) and `typing-extensions>=4.12.2,<5` (previously no
  upper bound). As a library, socketdev declares bounded ranges rather than
  exact pins so its constraints compose with consumers that pin their own
  dependencies, such as the Socket Python CLI.
- Pinned the `hatchling` build backend used for sdist builds.

---

Entries below are imported from the auto-generated
[GitHub release notes](https://github.com/SocketDev/socket-sdk-python/releases).

## 3.4.2 (2026-08-05)

### What's Changed
* ci(deps): bump pypa/gh-action-pypi-publish from ab69e431e9c9f48a3310be0a56527c679f56e04d to dc37677b2e1c63e2034f94d8a5b11f265b73ba33 by @dependabot[bot] in https://github.com/SocketDev/socket-sdk-python/pull/91
* ci(deps): bump actions/checkout from 6.0.2 to 7.0.1 by @dependabot[bot] in https://github.com/SocketDev/socket-sdk-python/pull/96
* chore(deps): bump the python-minor-patch group across 1 directory with 2 updates by @dependabot[bot] in https://github.com/SocketDev/socket-sdk-python/pull/95
* Make SDK preview publication opt-in by @lelia in https://github.com/SocketDev/socket-sdk-python/pull/100
* Add missing purl types and per-artifact parse resilience to full-scan stream by @lelia in https://github.com/SocketDev/socket-sdk-python/pull/101
* Add cached diff-scan polling support to DiffScans.get by @lelia in https://github.com/SocketDev/socket-sdk-python/pull/99
* fix(purl): expose fail-open batch params and harden dedupe by @lelia in https://github.com/SocketDev/socket-sdk-python/pull/98


**Full Changelog**: https://github.com/SocketDev/socket-sdk-python/compare/v3.3.0...v3.4.2

## 3.3.0 (2026-06-10)

### What's Changed
* Add transient-error classification to APIFailure by @mtorp in https://github.com/SocketDev/socket-sdk-python/pull/93


**Full Changelog**: https://github.com/SocketDev/socket-sdk-python/compare/v3.2.1...v3.3.0

## 3.2.1 (2026-06-03)

### What's Changed
* Add `sfw` aggregator gate to enforce required CI checks by @lelia in https://github.com/SocketDev/socket-sdk-python/pull/89


**Full Changelog**: https://github.com/SocketDev/socket-sdk-python/compare/v3.2.0...v3.2.1

## 3.2.0 (2026-06-03)

### What's Changed
* Add `OTHER` category to SocketCategory enum by @lelia in https://github.com/SocketDev/socket-sdk-python/pull/85
* ci(deps): bump actions/setup-python from 5.2.0 to 6.2.0 by @dependabot[bot] in https://github.com/SocketDev/socket-sdk-python/pull/86
* ci(deps): bump actions/github-script from 7.0.1 to 9.0.0 by @dependabot[bot] in https://github.com/SocketDev/socket-sdk-python/pull/87
* chore(deps): bump the python-minor-patch group with 2 updates by @dependabot[bot] in https://github.com/SocketDev/socket-sdk-python/pull/88


**Full Changelog**: https://github.com/SocketDev/socket-sdk-python/compare/v3.1.2...v3.2.0

## 3.1.2 (2026-06-02)

### What's Changed
* Dependabot hardening + dependency update bundle by @lelia in https://github.com/SocketDev/socket-sdk-python/pull/84


**Full Changelog**: https://github.com/SocketDev/socket-sdk-python/compare/v3.1.1...v3.1.2

## 3.1.1 (2026-05-22)

### What's Changed
* ci(version-check): require uv.lock sync alongside pyproject changes by @flowstate in https://github.com/SocketDev/socket-sdk-python/pull/82
* Fix stale `didYouMean` props by @flowstate in https://github.com/SocketDev/socket-sdk-python/pull/81


**Full Changelog**: https://github.com/SocketDev/socket-sdk-python/compare/v3.1.0...v3.1.1

## 3.1.0 (2026-05-21)

### What's Changed
* Support org-scoped batch package endpoint by @lelia in https://github.com/SocketDev/socket-sdk-python/pull/76


**Full Changelog**: https://github.com/SocketDev/socket-sdk-python/compare/v3.0.33...v3.1.0

## 3.0.33 (2026-04-24)

### What's Changed
* fix: harden GitHub Actions workflows by @reberhardt7 in https://github.com/SocketDev/socket-sdk-python/pull/72
* fix: tolerate unknown SocketCategory values in SocketAlert.from_dict by @dc-larsen in https://github.com/SocketDev/socket-sdk-python/pull/79

### New Contributors
* @reberhardt7 made their first contribution in https://github.com/SocketDev/socket-sdk-python/pull/72
* @dc-larsen made their first contribution in https://github.com/SocketDev/socket-sdk-python/pull/79

**Full Changelog**: https://github.com/SocketDev/socket-sdk-python/compare/v3.0.32...v3.0.33

## 3.0.32 (2026-02-27)

### What's Changed
* Fixing issue where incorrect workspace was being set as None by @dacoburn in https://github.com/SocketDev/socket-sdk-python/pull/71


**Full Changelog**: https://github.com/SocketDev/socket-sdk-python/compare/v3.0.31...v3.0.32

## 3.0.31 (2026-02-26)

### What's Changed
* Bump urllib3 from 2.6.2 to 2.6.3 by @dependabot[bot] in https://github.com/SocketDev/socket-sdk-python/pull/67
* Bump virtualenv from 20.35.4 to 20.36.1 by @dependabot[bot] in https://github.com/SocketDev/socket-sdk-python/pull/66
* Bump cryptography from 46.0.3 to 46.0.5 by @dependabot[bot] in https://github.com/SocketDev/socket-sdk-python/pull/69
* Add `workspace` param support by @lelia in https://github.com/SocketDev/socket-sdk-python/pull/68
* Update CODEOWNERS to reflect team ownership by @lelia in https://github.com/SocketDev/socket-sdk-python/pull/70

### New Contributors
* @dependabot[bot] made their first contribution in https://github.com/SocketDev/socket-sdk-python/pull/67
* @lelia made their first contribution in https://github.com/SocketDev/socket-sdk-python/pull/68

**Full Changelog**: https://github.com/SocketDev/socket-sdk-python/compare/v3.0.29...v3.0.31

## 3.0.29 (2026-01-21)

### What's Changed
* Add scan_type query param to full scan API by @mtorp in https://github.com/SocketDev/socket-sdk-python/pull/64


**Full Changelog**: https://github.com/SocketDev/socket-sdk-python/compare/v3.0.28...v3.0.29

## 3.0.28 (2026-01-05)

### What's Changed
* Updating README with latest changes by @dacoburn in https://github.com/SocketDev/socket-sdk-python/pull/63
* Updated README with new Slack bot directions by @dacoburn in https://github.com/SocketDev/socket-sdk-python/pull/65


**Full Changelog**: https://github.com/SocketDev/socket-sdk-python/compare/v3.0.25...v3.0.28

## 3.0.25 (2026-01-01)

### What's Changed
* Added option to override user agent string by @dacoburn in https://github.com/SocketDev/socket-sdk-python/pull/62


**Full Changelog**: https://github.com/SocketDev/socket-sdk-python/compare/v3.0.24...v3.0.25

## 3.0.24 (2026-01-01)

### What's Changed
* Upgraded dependencies and fixed versioning by @dacoburn in https://github.com/SocketDev/socket-sdk-python/pull/61


**Full Changelog**: https://github.com/SocketDev/socket-sdk-python/compare/v3.0.23...v3.0.24

## 3.0.23 (2026-01-01)

### What's Changed
* feat: Add comprehensive SDK enhancements and new endpoint modules by @dacoburn in https://github.com/SocketDev/socket-sdk-python/pull/60


**Full Changelog**: https://github.com/SocketDev/socket-sdk-python/compare/v3.0.22...v3.0.23

## 3.0.22 (2025-12-10)

### What's Changed
* Changed version to be optional so that if it isn't there in a diff or… by @dacoburn in https://github.com/SocketDev/socket-sdk-python/pull/59


**Full Changelog**: https://github.com/SocketDev/socket-sdk-python/compare/v3.0.21...v3.0.22

## 3.0.21 (2025-11-27)

### What's Changed
* create function for finalizing Tier 1 reachability analyses by @mtorp in https://github.com/SocketDev/socket-sdk-python/pull/58

### New Contributors
* @mtorp made their first contribution in https://github.com/SocketDev/socket-sdk-python/pull/58

**Full Changelog**: https://github.com/SocketDev/socket-sdk-python/compare/v3.0.20...v3.0.21

## 3.0.20 (2025-11-15)

### What's Changed
* Fixing versioning as didn't add project files in last branch by @dacoburn in https://github.com/SocketDev/socket-sdk-python/pull/57


**Full Changelog**: https://github.com/SocketDev/socket-sdk-python/compare/v3.0.19...v3.0.20

## 3.0.19 (2025-11-15)

### What's Changed
* Doug/add unverified option by @dacoburn in https://github.com/SocketDev/socket-sdk-python/pull/56


**Full Changelog**: https://github.com/SocketDev/socket-sdk-python/compare/v3.0.17...v3.0.19

## 3.0.17 (2025-11-07)

### What's Changed
* Fixed logic for upload manifest files to not strip the folder names f… by @dacoburn in https://github.com/SocketDev/socket-sdk-python/pull/55


**Full Changelog**: https://github.com/SocketDev/socket-sdk-python/compare/v3.0.16...v3.0.17

## 3.0.16 (2025-11-07)

### What's Changed
* Added upload manifests endpoint for reachability by @dacoburn in https://github.com/SocketDev/socket-sdk-python/pull/54


**Full Changelog**: https://github.com/SocketDev/socket-sdk-python/compare/v3.0.14...v3.0.16

## 3.0.14 (2025-10-17)

### What's Changed
* Fix the normalization for file names to work for specifying a file, p… by @dacoburn in https://github.com/SocketDev/socket-sdk-python/pull/53


**Full Changelog**: https://github.com/SocketDev/socket-sdk-python/compare/v3.0.13...v3.0.14

## 3.0.13 (2025-10-14)

### What's Changed
* Fixing workflows with pinned versions by @dacoburn in https://github.com/SocketDev/socket-sdk-python/pull/50
* Update action versions in pr-preview.yml by @dacoburn in https://github.com/SocketDev/socket-sdk-python/pull/51
* Update PyPI publish action version by @dacoburn in https://github.com/SocketDev/socket-sdk-python/pull/52
* Fix dedupe logic to work with compact mode for the purl endpoint by @dacoburn in https://github.com/SocketDev/socket-sdk-python/pull/49


**Full Changelog**: https://github.com/SocketDev/socket-sdk-python/compare/v3.0.6...v3.0.13

## 3.0.6 (2025-09-12)

### What's Changed
* feat: Add support for base_paths parameter in fullscans and diffscans by @dacoburn in https://github.com/SocketDev/socket-sdk-python/pull/48


**Full Changelog**: https://github.com/SocketDev/socket-sdk-python/compare/v3.0.5...v3.0.6

## 3.0.5 (2025-09-09)

### What's Changed
* fix: Align SDK endpoints and tests with OpenAPI spec by @dacoburn in https://github.com/SocketDev/socket-sdk-python/pull/47


**Full Changelog**: https://github.com/SocketDev/socket-sdk-python/compare/v3.0.4...v3.0.5

## 3.0.4 (2025-09-03)

### What's Changed
* feat: Complete API endpoint coverage with comprehensive tests and doc… by @dacoburn in https://github.com/SocketDev/socket-sdk-python/pull/45


**Full Changelog**: https://github.com/SocketDev/socket-sdk-python/compare/v3.0.2...v3.0.4

## 3.0.2 (2025-08-24)

### What's Changed
* Fix README typos by @Planeshifter in https://github.com/SocketDev/socket-sdk-python/pull/43
* fix: include namespace in deduplicated purl construction by @dacoburn in https://github.com/SocketDev/socket-sdk-python/pull/44

### New Contributors
* @Planeshifter made their first contribution in https://github.com/SocketDev/socket-sdk-python/pull/43

**Full Changelog**: https://github.com/SocketDev/socket-sdk-python/compare/v3.0.0...v3.0.2

## 3.0.0 (2025-08-23)

### What's Changed
* feat: migrate to socketdev 3.0.0 and switch to uv dependency management by @dacoburn in https://github.com/SocketDev/socket-sdk-python/pull/42


**Full Changelog**: https://github.com/SocketDev/socket-sdk-python/compare/v2.2.3...v3.0.0

## 2.2.3 (2025-08-23)

### What's Changed
* Adding deprecation notice by @dacoburn in https://github.com/SocketDev/socket-sdk-python/pull/41


**Full Changelog**: https://github.com/SocketDev/socket-sdk-python/compare/v2.1.8...v2.2.3

## 2.1.8 (2025-08-22)

### What's Changed
* Doug/fix diff scan license options by @dacoburn in https://github.com/SocketDev/socket-sdk-python/pull/40


**Full Changelog**: https://github.com/SocketDev/socket-sdk-python/compare/v2.1.5...v2.1.8

## 2.1.5 (2025-06-20)

### What's Changed
* Improvements to unit tests for new diff scans by @dacoburn in https://github.com/SocketDev/socket-sdk-python/pull/39


**Full Changelog**: https://github.com/SocketDev/socket-sdk-python/compare/v2.1.4...v2.1.5

## 2.1.4 (2025-06-10)

### What's Changed
* Added missing property by @dacoburn in https://github.com/SocketDev/socket-sdk-python/pull/38


**Full Changelog**: https://github.com/SocketDev/socket-sdk-python/compare/v2.1.3...v2.1.4

## 2.1.3 (2025-06-09)

### What's Changed
* Fixed logging to use logging instead of print by @dacoburn in https://github.com/SocketDev/socket-sdk-python/pull/37


**Full Changelog**: https://github.com/SocketDev/socket-sdk-python/compare/v2.1.0...v2.1.3

## 2.1.0 (2025-06-02)

### What's Changed
* Doug/add new endpoints by @dacoburn in https://github.com/SocketDev/socket-sdk-python/pull/36


**Full Changelog**: https://github.com/SocketDev/socket-sdk-python/compare/v2.0.22...v2.1.0

## 2.0.22 (2025-04-25)

### What's Changed
* Fixed the logic for dedeupe and ths missing alert fields by @dacoburn in https://github.com/SocketDev/socket-sdk-python/pull/35


**Full Changelog**: https://github.com/SocketDev/socket-sdk-python/compare/v2.0.21...v2.0.22

## 2.0.21 (2025-04-03)

### What's Changed
* Fix attributes being dropped during dedupe by @dacoburn in https://github.com/SocketDev/socket-sdk-python/pull/34


**Full Changelog**: https://github.com/SocketDev/socket-sdk-python/compare/v2.0.20...v2.0.21

## 2.0.20 (2025-04-01)

### What's Changed
* Doug/add dedupe logic to sdk by @dacoburn in https://github.com/SocketDev/socket-sdk-python/pull/33


**Full Changelog**: https://github.com/SocketDev/socket-sdk-python/compare/v2.0.16...v2.0.20

## 2.0.16 (2025-03-31)

### What's Changed
* Fixed purl logic to accept params by @dacoburn in https://github.com/SocketDev/socket-sdk-python/pull/31


**Full Changelog**: https://github.com/SocketDev/socket-sdk-python/compare/v2.0.15...v2.0.16

## 2.0.15 (2025-03-24)

### What's Changed
* Fixed deployment process to ensure the versions are being pushed to pypi by @dacoburn in https://github.com/SocketDev/socket-sdk-python/pull/30


**Full Changelog**: https://github.com/SocketDev/socket-sdk-python/compare/v2.0.14...v2.0.15

## 2.0.14 (2025-03-24)

### What's Changed
* Doug/fix api error by @dacoburn in https://github.com/SocketDev/socket-sdk-python/pull/29


**Full Changelog**: https://github.com/SocketDev/socket-sdk-python/compare/v2.0.13...v2.0.14

## 2.0.13 (2025-03-19)

### What's Changed
* Doug/make params url safe by @dacoburn in https://github.com/SocketDev/socket-sdk-python/pull/28


**Full Changelog**: https://github.com/SocketDev/socket-sdk-python/compare/v2.0.11...v2.0.13

## 2.0.11 (2025-03-15)

### What's Changed
* Add support for include_license_details for the streaming diff endpoint by @dacoburn in https://github.com/SocketDev/socket-sdk-python/pull/27


**Full Changelog**: https://github.com/SocketDev/socket-sdk-python/compare/v2.0.10...v2.0.11

## 2.0.10 (2025-03-13)

### What's Changed
* Doug/fix missing repo field by @dacoburn in https://github.com/SocketDev/socket-sdk-python/pull/26


**Full Changelog**: https://github.com/SocketDev/socket-sdk-python/compare/v2.0.9...v2.0.10

## 2.0.9 (2025-02-28)

### What's Changed
* Fix for the validation test being in the get instead of post by @dacoburn in https://github.com/SocketDev/socket-sdk-python/pull/24


**Full Changelog**: https://github.com/SocketDev/socket-sdk-python/compare/v2.0.8...v2.0.9

## 2.0.8 (2025-02-27)

### What's Changed
* Return headers on request exception by @flowstate in https://github.com/SocketDev/socket-sdk-python/pull/23


**Full Changelog**: https://github.com/SocketDev/socket-sdk-python/compare/v2.0.7...v2.0.8

## 2.0.7 (2025-02-25)

### What's Changed
* improved error handling by @flowstate in https://github.com/SocketDev/socket-sdk-python/pull/22


**Full Changelog**: https://github.com/SocketDev/socket-sdk-python/compare/v2.0.6...v2.0.7

## 2.0.6 (2025-02-24)

### What's Changed
* Fix for params already being a dict by @dacoburn in https://github.com/SocketDev/socket-sdk-python/pull/21


**Full Changelog**: https://github.com/SocketDev/socket-sdk-python/compare/v2.0.5...v2.0.6

## 2.0.5 (2025-02-14)

### What's Changed
* small fixes to support CLI bugfixes @flowstate in https://github.com/SocketDev/socket-sdk-python/pull/20


**Full Changelog**: https://github.com/SocketDev/socket-sdk-python/compare/v2.0.4...v2.0.5

## 2.0.4 (2025-02-12)

### What's Changed
* updated type definitions and logic to align with the updates to the Socket API (diff endpoint)


**Full Changelog**: https://github.com/SocketDev/socket-sdk-python/compare/v2.0.2...v2.0.4

## 2.0.2 (2025-02-06)

_No release notes provided._

## 2.0.1 (2025-02-06, pre-release)

### What's Changed
* github workflow improvements and python version compatibility updates by @flowstate in https://github.com/SocketDev/socket-sdk-python/pull/17


**Full Changelog**: https://github.com/SocketDev/socket-sdk-python/compare/v2.0.0...v2.0.1

## 2.0.0 (2025-02-05, pre-release)

### What's Changed
- Version bumped to 2 to indicate potentially breaking changes
- Typing was added to most endpoints (specifically those used by the python CLI)

- Since this is such a large change-set, we aren't suggesting everyone move to v2 immediately. If you do, and run into any bugs, please open an issue so we can address them.

**Full Changelog**: https://github.com/SocketDev/socket-sdk-python/compare/v1.0.15...v2.0.0

## 1.0.15 (2025-01-24)

### What's Changed
* Initial code by @dacoburn in https://github.com/SocketDev/socket-sdk-python/pull/1
* Orlando/add new endpoints by @obarrera in https://github.com/SocketDev/socket-sdk-python/pull/2
* Adding code owners file by @dacoburn in https://github.com/SocketDev/socket-sdk-python/pull/3
* Added the Purl API endpoint by @obarrera in https://github.com/SocketDev/socket-sdk-python/pull/4
* Orgs full scans by @obarrera in https://github.com/SocketDev/socket-sdk-python/pull/5
* Update README.rst by @obarrera in https://github.com/SocketDev/socket-sdk-python/pull/6
* Doug/add new features by @dacoburn in https://github.com/SocketDev/socket-sdk-python/pull/7
* Added missing endpoints and updated documentation by @dacoburn in https://github.com/SocketDev/socket-sdk-python/pull/8
* Fixed issue in the newly added endpoints by @dacoburn in https://github.com/SocketDev/socket-sdk-python/pull/9
* Add the missing folder to the by @dacoburn in https://github.com/SocketDev/socket-sdk-python/pull/10
* added endpoints to python sdk by @flowstate in https://github.com/SocketDev/socket-sdk-python/pull/11
* fixed build script and README formatting by @flowstate in https://github.com/SocketDev/socket-sdk-python/pull/12
* hotfix - add export to socketdev and toml by @flowstate in https://github.com/SocketDev/socket-sdk-python/pull/13
* added pr-preview and release workflows by @flowstate in https://github.com/SocketDev/socket-sdk-python/pull/15
* updated load_files to omit the path to workspace if specified by @flowstate in https://github.com/SocketDev/socket-sdk-python/pull/16

### New Contributors
* @dacoburn made their first contribution in https://github.com/SocketDev/socket-sdk-python/pull/1
* @obarrera made their first contribution in https://github.com/SocketDev/socket-sdk-python/pull/2
* @flowstate made their first contribution in https://github.com/SocketDev/socket-sdk-python/pull/11

**Full Changelog**: https://github.com/SocketDev/socket-sdk-python/commits/v1.0.15

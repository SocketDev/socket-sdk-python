# Changelog

## 3.4.3

### Changed: bound runtime dependency ranges and pin build backend

- Added version bounds to the runtime dependencies: `requests>=2.32.5,<3`
  (previously unbounded) and `typing-extensions>=4.12.2,<5` (previously no
  upper bound). As a library, socketdev declares bounded ranges rather than
  exact pins so its constraints compose with consumers that pin their own
  dependencies, such as the Socket Python CLI.
- Pinned the `hatchling` build backend used for sdist builds.

---

Releases prior to 3.4.3 predate this changelog. See the
[GitHub releases](https://github.com/SocketDev/socket-sdk-python/releases)
for earlier release notes.

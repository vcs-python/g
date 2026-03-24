# Releasing

## Release Process

Releases are triggered by git tags and published to PyPI via OIDC trusted publishing.

1. Update `CHANGES` with the release notes

2. Bump version in `src/g/__about__.py` (or wherever version is defined -- check pyproject.toml)

3. Tag:

   ```console
   $ git tag v<version>
   ```

4. Push:

   ```console
   $ git push && git push --tags
   ```

5. CI builds and publishes to PyPI automatically

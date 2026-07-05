# Releasing

## Release Process

Use this page when you are preparing a g release. Tags trigger publishing to
[PyPI] via [OIDC] trusted publishing, so create and push them only when you
intend to publish.

1. Update `CHANGES` with the release notes

2. Bump the version in `src/g/__about__.py` and `pyproject.toml`

3. Commit the release files with the subject `Tag v<version>`

4. Tag:

   ```console
   $ git tag v<version>
   ```

5. Push the branch:

   ```console
   $ git push
   ```

6. Push the tag:

   ```console
   $ git push --tags
   ```

7. CI builds and publishes to PyPI automatically

For AI agents: do not create or push tags unless the user explicitly asks.
Prepare the release files and commit only.

[OIDC]: https://openid.net/developers/how-connect-works/
[PyPI]: https://pypi.org/

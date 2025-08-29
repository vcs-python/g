# Testing the Cookiecutter Template

This directory contains tests for the cookiecutter template. The tests use [pytest-cookies](https://github.com/hackebrot/pytest-cookies), a pytest plugin for testing cookiecutter templates.

## Running the Tests

1. Install pytest and pytest-cookies:

```bash
pip install pytest pytest-cookies
```

2. Run the tests:

```bash
pytest -xvs tests/test_cookiecutter.py
```

Alternatively, if you're using `uv` (the fast Python package installer and resolver):

```bash
uv run pytest -xvs tests/test_cookiecutter.py
```

## Test Overview

The tests in `test_cookiecutter.py` cover the following scenarios:

1. **Default template generation**: Tests that the template generates correctly with default values.
2. **Test execution in generated project**: Tests that the generated project's own tests run successfully.
3. **VCS path registry**: Tests proper configuration of supported version control systems.
4. **License file generation**: Tests that the correct license file is generated based on selection.
5. **GitHub Actions workflow creation**: Tests optional GitHub Actions workflow generation.
6. **Documentation creation**: Tests optional documentation generation.
7. **pyproject.toml configuration**: Tests proper project metadata configuration.
8. **README badge inclusion**: Tests conditional inclusion of status badges in README.
9. **Package structure**: Tests proper Python package directory structure.

## Debugging

If you encounter issues with the tests, you can keep the generated projects for inspection by adding the `--keep-baked-projects` flag:

```bash
pytest -xvs tests/test_cookiecutter.py --keep-baked-projects
```

This can be helpful for debugging test failures as you can inspect the actual generated files. 
# `$ {{cookiecutter.package_name}}`

{{cookiecutter.project_description}}

[![Python Package](https://img.shields.io/pypi/v/{{cookiecutter.package_name}}.svg)](https://pypi.org/project/{{cookiecutter.package_name}}/)
{% if cookiecutter.include_docs == "y" %}
[![Docs](https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.github_repo}}/workflows/docs/badge.svg)](https://{{cookiecutter.package_name}}.git-pull.com)
{% endif %}
{% if cookiecutter.include_github_actions == "y" %}
[![Build Status](https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.github_repo}}/workflows/tests/badge.svg)](https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.github_repo}}/actions?query=workflow%3A%22tests%22)
[![Code Coverage](https://codecov.io/gh/{{cookiecutter.github_username}}/{{cookiecutter.github_repo}}/branch/master/graph/badge.svg)](https://codecov.io/gh/{{cookiecutter.github_username}}/{{cookiecutter.github_repo}})
{% endif %}
[![License](https://img.shields.io/github/license/{{cookiecutter.github_username}}/{{cookiecutter.github_repo}}.svg)](https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.github_repo}}/blob/master/LICENSE)

Shortcut / powertool for developers to access current repos' VCS, whether it's
{% for vcs in cookiecutter.supported_vcs.split(',') %}
{% if loop.first %}{{vcs.strip()}}{% elif loop.last %} or {{vcs.strip()}}{% else %}, {{vcs.strip()}}{% endif %}{% endfor %}.

```console
$ pip install --user {{cookiecutter.package_name}}
```

```console
$ {{cookiecutter.package_name}}
```

### Developmental releases

You can test the unpublished version of {{cookiecutter.package_name}} before its released.

- [pip](https://pip.pypa.io/en/stable/):

  ```console
  $ pip install --user --upgrade --pre {{cookiecutter.package_name}}
  ```

- [pipx](https://pypa.github.io/pipx/docs/):

  ```console
  $ pipx install --suffix=@next {{cookiecutter.package_name}} --pip-args '\--pre' --force
  ```

  Then use `{{cookiecutter.package_name}}@next --help`.

# More information

- Python support: >= {{cookiecutter.python_version}}, pypy
- VCS supported: {% for vcs in cookiecutter.supported_vcs.split(',') %}{{vcs.strip()}}(1){% if not loop.last %}, {% endif %}{% endfor %}
- Source: <https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.github_repo}}>
{% if cookiecutter.include_docs == "y" %}
- Docs: <https://{{cookiecutter.package_name}}.git-pull.com>
- Changelog: <https://{{cookiecutter.package_name}}.git-pull.com/history.html>
- API: <https://{{cookiecutter.package_name}}.git-pull.com/api.html>
{% endif %}
- Issues: <https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.github_repo}}/issues>
{% if cookiecutter.include_github_actions == "y" %}
- Test Coverage: <https://codecov.io/gh/{{cookiecutter.github_username}}/{{cookiecutter.github_repo}}>
{% endif %}
- pypi: <https://pypi.python.org/pypi/{{cookiecutter.package_name}}>
- License: [{{cookiecutter.license}}](https://opensource.org/licenses/{{cookiecutter.license}}) 
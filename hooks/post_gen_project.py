#!/usr/bin/env python
"""Post-generation script for cookiecutter."""

import os
import datetime

license_type = "{{cookiecutter.license}}"
author = "{{cookiecutter.author_name}}"
year = datetime.datetime.now().year


def generate_mit_license():
    """Generate MIT license file."""
    mit_license = f"""MIT License

Copyright (c) {year} {author}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
    with open("LICENSE", "w") as f:
        f.write(mit_license)


def generate_bsd3_license():
    """Generate BSD-3 license file."""
    bsd3_license = f"""BSD 3-Clause License

Copyright (c) {year}, {author}
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
    with open("LICENSE", "w") as f:
        f.write(bsd3_license)


def generate_gpl3_license():
    """Generate GPL-3.0 license file."""
    # This would be the full GPL-3.0 license, but it's very long
    # Here we'll just write a reference to the standard license
    gpl3_license = f"""Copyright (C) {year} {author}

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
    with open("LICENSE", "w") as f:
        f.write(gpl3_license)


def generate_apache2_license():
    """Generate Apache-2.0 license file."""
    apache2_license = f"""                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   Copyright {year} {author}

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
    with open("LICENSE", "w") as f:
        f.write(apache2_license)


if __name__ == "__main__":
    if license_type == "MIT":
        generate_mit_license()
    elif license_type == "BSD-3":
        generate_bsd3_license()
    elif license_type == "GPL-3.0":
        generate_gpl3_license()
    elif license_type == "Apache-2.0":
        generate_apache2_license()
    else:
        print(f"Unsupported license type: {license_type}")

    # Create test directory if tests are included
    if "{{cookiecutter.include_tests}}" == "y":
        if not os.path.exists("tests"):
            os.makedirs("tests")
            with open("tests/__init__.py", "w") as f:
                f.write("""Test package for {{cookiecutter.package_name}}.""")
            
            # Create a basic test file
            with open("tests/test_cli.py", "w") as f:
                f.write("""#!/usr/bin/env python
"""Test CLI for {{cookiecutter.package_name}}."""

from __future__ import annotations

import os
import pathlib
import subprocess
import sys

import pytest

import {{cookiecutter.package_name}}


def test_run():
    """Test run."""
    # Test that the function doesn't error
    proc = {{cookiecutter.package_name}}.run(cmd="echo", cmd_args=["hello"])
    assert proc is None

    # Test when G_IS_TEST is set, it returns the proc
    os.environ["{{cookiecutter.package_name.upper()}}_IS_TEST"] = "1"
    proc = {{cookiecutter.package_name}}.run(cmd="echo", cmd_args=["hello"])
    assert isinstance(proc, subprocess.Popen)
    assert proc.returncode == 0
    del os.environ["{{cookiecutter.package_name.upper()}}_IS_TEST"]
""")

    # Create docs directory if docs are included
    if "{{cookiecutter.include_docs}}" == "y":
        if not os.path.exists("docs"):
            os.makedirs("docs")
            with open("docs/index.md", "w") as f:
                f.write("""# {{cookiecutter.project_name}}

{{cookiecutter.project_description}}

## Installation

```bash
pip install {{cookiecutter.package_name}}
```

## Usage

```bash
{{cookiecutter.package_name}}
```

This will detect the type of repository in your current directory and run the appropriate VCS command.
""")

    # Create GitHub Actions workflows if included
    if "{{cookiecutter.include_github_actions}}" == "y":
        if not os.path.exists(".github/workflows"):
            os.makedirs(".github/workflows")
            with open(".github/workflows/tests.yml", "w") as f:
                f.write("""name: tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11']

    steps:
      - uses: actions/checkout@v3
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install uv
          uv pip install -e .
          uv pip install pytest pytest-cov
      - name: Test with pytest
        run: |
          uv pip install pytest
          pytest
""")

    print("Project generated successfully!") 
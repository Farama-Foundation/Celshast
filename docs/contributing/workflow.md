# Workflow

This page describes the tooling used during development of this project. It also serves as a reference for the various commands that you would use when working on this project.

## Overview

This project uses the [GitHub Flow] for collaboration. The codebase contains Python code, [Jinja2]-based HTML pages, [Sass] stylesheets and Javascript code.

- [mise] pins the toolchain (`python`, `node`, `uv`, `just`) so contributors get matching versions.
- [uv] backs [nox]'s session venvs (configured in `noxfile.py`) for fast installs.
- [just] provides short aliases for common tasks (see `Justfile`).
- [Webpack]-based build pipeline is used to process the Sass and Javascript files.
- [sphinx-autobuild] is used to provide live-reloading pages when working on the theme.
- [pre-commit] runs the linters: [ruff] (lint + format) plus [prettier], [blacken-docs], [mypy], and a few `pre-commit-hooks` checks.

## Initial Setup

To work on this project, you need git 2.17+. The Python, Node, `uv`, and `just` versions are pinned in `mise.toml` and provisioned by mise.

- Clone this project using git:

  ```
  git clone https://github.com/pradyunsg/furo.git
  cd furo
  ```

- Install [mise] (https://mise.jdx.dev/) and provision the pinned toolchain:

  ```
  mise install
  ```

That installs Python, Node, `uv`, and `just` at the versions in `mise.toml`. `nox` is invoked through `uvx`, so there's nothing else to install up front.

## Commands

The recipes in the `Justfile` wrap the most common nox sessions. Either form works.

### Code Linting

```
just lint
# or: uvx nox -s lint
```

Run the linters, as configured with [pre-commit]. Python linting and formatting are handled by [ruff] (the config lives in `pyproject.toml` under `[tool.ruff]`).

### Local Development Server

```
just serve
# or: uvx nox -s docs-live
```

Serve this project's documentation locally, using [sphinx-autobuild]. This will open the generated documentation page in your browser.

`just serve` binds to `0.0.0.0:8000` by default so the docs are reachable from another device on your LAN (e.g. a phone). To change the host or port:

```
just serve 127.0.0.1 9000
```

Or pass any `stb serve` flag through nox:

```
uvx nox -s docs-live -- --host 127.0.0.1 --port 9000
```

The server also watches for changes made to the documentation (`docs/`) or theme (`src/`), which will trigger a rebuild. Once the build is completed, server will automagically reload any open pages using livereload.

:::{tip}
My workflow, when I'm working on this theme, is along the lines of:

- Run this command, and wait for the browser window to open.
- <kbd>alt</kbd>+<kbd>tab</kbd> gets me back to my text editor.
- Make changes to some files and save those changes.
- <kbd>alt</kbd>+<kbd>tab</kbd> switches to the browser.
- After a small delay, the change is reflected in the browser.
- If I want to make more changes, <kbd>alt</kbd>+<kbd>tab</kbd> and I'm back to my text editor.
- Repeat the previous 4 steps until happy.

\- @pradyunsg
:::

### Documentation Generation

```
just build
# or: uvx nox -s docs
```

Generate the documentation for Furo into the `build/docs` folder. This (mostly) does the same thing as `docs-live`, except it invokes `sphinx-build` instead of [sphinx-autobuild].

## Release process

- Update the changelog
- Run `uvx nox -s release`
- Once that command succeeds, you're done!

## Installing directly from GitHub

There are times when you might want to install the in-development version of Furo (mostly for testing that a fix actually does fix things).

This can be done by directly telling pip to install from Furo from GitHub. You likely want to install from a zip archive, to avoid cloning the entire Git history:

```sh
pip install https://github.com/pradyunsg/furo/archive/refs/heads/main.zip
```

[github flow]: https://guides.github.com/introduction/flow/
[mise]: https://mise.jdx.dev/
[uv]: https://docs.astral.sh/uv/
[just]: https://github.com/casey/just
[nox]: https://nox.readthedocs.io/en/stable/
[jinja2]: https://jinja.palletsprojects.com
[sass]: https://sass-lang.com
[webpack]: https://webpack.js.org/
[sphinx-autobuild]: https://github.com/executablebooks/sphinx-autobuild
[pre-commit]: https://pre-commit.com/
[ruff]: https://docs.astral.sh/ruff/
[prettier]: https://prettier.io/
[blacken-docs]: https://github.com/asottile/blacken-docs
[mypy]: https://mypy.readthedocs.io/

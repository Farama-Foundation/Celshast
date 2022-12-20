# Celshast

A [Farama Foundation](https://farama.org/) <a href="https://www.sphinx-doc.org/">Sphinx</a> documentation theme based on the [Furo template](https://github.com/pradyunsg/furo).

## Building Theme from source

```
pip install nox
```

```
nox -s docs-live
```

## Google Analytics

To enable Google Analytics add the following theme option in the `conf.py` file.

``` python
html_theme_options = {
    "gtag": "G-6H9C8TWXZ8",
}
```

## Versioning

Celshast supports documentation versioning using an HTML menu and GitHub Actions. Every page has a JS script that injects an html document with the [versions menu](https://github.com/Farama-Foundation/Celshast/blob/main/src/furo/theme/furo/static/versioning/versioning_menu.html), which allows updating older versions without rebuilding.

To enable the menu set the theme option to true in the `conf.py` file:

``` python
html_theme_options = {
    "versioning": True,
}
```

With versioning enabled you should have three different GitHub Actions workflows (the names are just an example):

* `build-dev.yml` - Build the docs based on the latest commit in the `main` branch, which is an unstable version. The build will be published in the folder `main` at the `gh-pages` branch.

``` yaml
name: Build main branch documentation website
on:
  push:
    branches: [main]
permissions:
  contents: write
jobs:
  docs:
    name: Generate Website
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - uses: actions/setup-python@v4
        with:
            python-version: '3.9'

      - name: Install dependencies
        run: pip install -r docs/requirements.txt

      - name: Install Gymnasium
        run: pip install mujoco && pip install .[atari,accept-rom-license,box2d]

      - name: Build Envs Docs
        run: python docs/scripts/gen_mds.py && python docs/scripts/gen_envs_display.py

      - name: Build
        run: sphinx-build -b dirhtml -v docs _build

      - name: Move 404
        run: mv _build/404/index.html _build/404.html

      - name: Update 404 links
        run: python docs/scripts/move_404.py _build/404.html

      - name: Remove .doctrees
        run: rm -r _build/.doctrees

      - name: Upload to GitHub Pages
        uses: JamesIves/github-pages-deploy-action@v4
        with:
          folder: _build
          target-folder: main
          clean: false
```

* `build-version.yml` - Build the docs' latest version based on a new release (tag). The build will be published in the root folder and a folder named after the version (e.g. 1.0.3) at the `gh-pages` branch.

``` yaml
name: Docs Versioning
on:
  push:
    tags:
      - 'v?*.*.*'
permissions:
  contents: write
jobs:
  docs:
    name: Generate Website for new version
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - uses: actions/setup-python@v4
        with:
            python-version: '3.9'

      - name: Get tag
        id: tag
        uses: dawidd6/action-get-tag@v1

      - name: Install docs dependencies
        run: pip install -r docs/requirements.txt

      - name: Install Gymnasium
        run: pip install mujoco && pip install .[atari,accept-rom-license,box2d]

      - name: Build Envs Docs
        run: python docs/scripts/gen_mds.py && python docs/scripts/gen_envs_display.py

      - name: Build
        run: sphinx-build -b dirhtml -v docs _build

      - name: Move 404
        run: mv _build/404/index.html _build/404.html

      - name: Update 404 links
        run: python docs/scripts/move_404.py _build/404.html

      - name: Remove .doctrees
        run: rm -r _build/.doctrees

      - name: Upload to GitHub Pages
        uses: JamesIves/github-pages-deploy-action@v4
        with:
          folder: _build
          target-folder: ${{steps.tag.outputs.tag}}
          clean: false

      - name: Upload to GitHub Pages
        uses: JamesIves/github-pages-deploy-action@v4
        with:
          folder: _build
          clean-exclude: |
            *.*.*/
            main
```

* `manual-build-version.yml` - Build a certain version of the documentation website based on a certain commit. The build will be published in the root folder (if the option latest is enabled) and a folder named after the version (e.g. 1.0.3) at the `gh-pages` branch.

``` yaml
name: Manual Docs Versioning
on:
  workflow_dispatch:
    inputs:
      version:
          description: 'Documentation version to create'
          required: true
      commit:
          description: 'Commit used to build the Documentation version'
          required: false
      latest:
          description: 'Latest version'
          type: boolean

permissions:
  contents: write
jobs:
  docs:
    name: Generate Website for new version
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        if: inputs.commit == ''

      - uses: actions/checkout@v3
        if: inputs.commit != ''
        with:
          ref: ${{ inputs.commit }}

      - uses: actions/setup-python@v4
        with:
            python-version: '3.9'

      - name: Install dependencies
        run: pip install -r docs/requirements.txt

      - name: Install Gymnasium
        run: pip install mujoco && pip install .[atari,accept-rom-license,box2d]

      - name: Build Envs Docs
        run: python docs/scripts/gen_mds.py && python docs/scripts/gen_envs_display.py

      - name: Build
        run: sphinx-build -b dirhtml -v docs _build

      - name: Move 404
        run: mv _build/404/index.html _build/404.html

      - name: Update 404 links
        run: python docs/scripts/move_404.py _build/404.html

      - name: Remove .doctrees
        run: rm -r _build/.doctrees

      - name: Upload to GitHub Pages
        uses: JamesIves/github-pages-deploy-action@v4
        with:
          folder: _build
          target-folder: ${{ inputs.version }}
          clean: false

      - name: Upload to GitHub Pages
        uses: JamesIves/github-pages-deploy-action@v4
        if: inputs.latest
        with:
          folder: _build
          clean-exclude: |
            *.*.*/
            main
```


## Edit page button

To enable the edit page button, which redirects the user to the source code of the page (i.e. markdown file), add the following context dictionary to the `conf.py` script.

``` python
html_context: Dict[str, Any] = {}
html_context["conf_py_path"] = "/docs/"
html_context["github_user"] = "Farama-Foundation"
html_context["github_repo"] = "Project Name"
html_context["github_version"] = "main" # (in some cases master)
```

## Disable Previous page and/or Next page buttons

If you don't want a certain page to have the `Next` and/or `Previous` buttons at the bottom you can disable them by adding the following variables to the front matter block of the markdown file:

* `firstpage:` - disables `Previous` button

* `lastpage:` - disables `Next` button

For example:
```
---
firstpage:
lastpage:
---
```

## Disable page edit button for autogenerated pages

Add the following variable to the front matter block of the markdown file:

```
---
autogenerated:
---
```

## Environment Icon

To add an icon next to the page title (H1 or H2, but it needs to be the first) add the following variable to the front matter block of the markdown file:

```
---
env_icon: [path to icon]
---
```


## Farama Top Menu

The Farama Foundation top menu is built using the response of the API [farama.org/api/projects.json](https://farama.org/api/projects.json). The source code of the API can found [here](https://github.com/Farama-Foundation/farama.org/blob/main/api/projects.json) and the source code of the menu [here](https://github.com/Farama-Foundation/Celshast/blob/main/src/furo/theme/furo/base.html#L238)
## Other Theme options

``` python
html_theme_options = {
    "light_logo": "img/gymnasium_black.svg",
    "dark_logo": "img/gymnasium_white.svg",
    "description": "A standard API for reinforcement learning and a diverse set of reference environments (formerly Gym)",
    "image": "img/gymnasium-github.png",
}
```

## Tutorials

We use [sphinx-gallery](https://sphinx-gallery.github.io/stable/index.html) to build the tutorials, however, due to an incompatibility of the library with Sphinx's `dirhtml` builder we have to resort to a workaround that is implemented in the theme. To add `sphinx-gallery` you need to add the following code to the `conf.py` script (assuming that all tutorials are in the folder `docs/tutorials`).

``` python
from furo import gen_tutorials
gen_tutorials.generate(
    os.path.dirname(__file__),
    os.path.join(os.path.dirname(__file__), "tutorials"),
)
```


## License

This project is licensed under the MIT License.

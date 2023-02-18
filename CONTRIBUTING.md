# Contribute to Farama projects documentation

Thank you for considering contributing to our documentation! A good
documentation is vital for any project and empowers those that use it.

Our documentation is written in [MyST (Markedly Structured Text)](https://myst-parser.readthedocs.io/en/latest/) and built using [Sphinx](https://www.sphinx-doc.org/en/master/).

Here are some important information about how to contribute to our documentation:

- [Build Documentation](./README.md#build-documentation)
- [Write Documentation](#write-documentation)
- [Write Environments Documentation](#write-environments-documentation)
- [Write Tutorials](#write-tutorials)
- [Sphinx Theme options](./README.md#theme-options)
- [Frontmatter options](./README.md#frontmatter)
- [Create Documentation Website](#create-a-documentation-website)

## Write Documentation

Here are some guidelines to follow when writing documentation:

1. Use **clear** and **concise** language. Avoid jargon and technical terms when possible.
2. Use **Google-style** Python docstrings.
3. Use the reStructuredText markup language inside docstrings.
4. Use [`autodoc`](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html) to automatically generate documentation from your code.
5. Use the MyST markdown (using the .md file extension) for documentation files inside the `docs/` directory.
6. Use scripts to generate environments documentation.
7. Use [`sphinx-gallery`](https://sphinx-gallery.github.io/stable/index.html) to include tutorials in your documentation.

## Write Environments Documentation

Environment documentation varies from project to project and sometimes from environment type.

Some environments, for example, Atari, require you to directly edit the Markdown file, however those are rare situations that should be **avoided**.

For most cases environments should be documented using a docstring inside the entry point class, [example](https://github.com/Farama-Foundation/Gymnasium/blob/5bb67ee69d8fc21fafe4147fdcafa1e1daf158c4/gymnasium/envs/box2d/bipedal_walker.py#L104). To automatically generate the documentation pages, i.e. `.md` files, you should use a python script, for example, [docs/scripts/gen_mds.py](https://github.com/Farama-Foundation/Gymnasium-Robotics/blob/main/docs/scripts/gen_mds.py).

## Write Tutorials

We use Sphinx-Gallery to build the tutorials inside the docs/tutorials directory.

To convert Jupyter Notebooks to Python tutorials you can use [this script](https://gist.github.com/mgoulao/f07f5f79f6cd9a721db8a34bba0a19a7).

If you want Sphinx-Gallery to execute the tutorial (which adds outputs and plots) then the file name should start with run_. Note that this adds to the build time so make sure the script doesn't take more than a few seconds to execute.

Go to [Sphinx-Gallery documentation](https://sphinx-gallery.github.io/stable/syntax.html) for more information.

## Create a Documentation website

* Create a directory named `docs` in the root directory of the project's repository
* **Copy** the contents inside the [start_kit](./starter_kit/) directory (you can use [donwload-directory.github.io](https://download-directory.github.io/?url=https%3A%2F%2Fgithub.com%2FFarama-Foundation%2FCelshast%2Ftree%2Fmain%2Fstarter_kit))
* **Paste** them inside the new `docs` directory
* Replace `<PROJECT>` and `<PROJECT_LOW>` with the name of the project, e.g. Gymnasiun would replace `<PROJECT>` with `Gymnasium` and `<PROJECT_LOW>` with `gymnasium`. You will find these placeholders inside files and in file names without the angle brackets.
* Replace the images and svg files inside `_static/img` with the ones corresponding to the project.
* Add content to the documentation.
* Add GitHub Actions workflows to build the website. Go [HERE](./README.md#versioning) for more information.

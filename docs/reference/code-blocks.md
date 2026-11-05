# Code Blocks

Code blocks and examples are an essential part of technical project documentation. Sphinx provides syntax highlighting for these out-of-the-box, through Pygments.

Celshast provides shared styling and installs [sphinx-copybutton], but projects must
enable the extension in `conf.py`:

```python
extensions = [
    # Other extensions...
    "sphinx_copybutton",
]

# Omit displayed line numbers and Pygments-marked console prompts from copies.
copybutton_exclude = ".linenos, .gp"
```

No additional documentation dependency is needed. A Sphinx theme is initialized
after configured extensions, too late to safely initialize another extension's
configuration, so Celshast deliberately does not activate it automatically. Projects
that already enable `sphinx-copybutton` require no integration changes.

Use the appropriate console lexer (such as `python-console`) so Pygments can identify
prompts such as `>>>` and `...`. Projects can extend the exclusion selector or use any
other [sphinx-copybutton configuration], for example:

```python
# conf.py
copybutton_exclude = ".linenos, .gp, .go"  # Also omit console output.
```

If a project has copy-button-specific CSS, remove rules that duplicate Celshast's
positioning, focus, color, or responsive target styles, keeping only intentional
project-specific customizations. The integration supports Celshast's supported Python
and Sphinx versions; non-HTML builders are not supported by the theme.

[sphinx-copybutton]: https://sphinx-copybutton.readthedocs.io/
[sphinx-copybutton configuration]: https://sphinx-copybutton.readthedocs.io/en/latest/use.html

````{furo-demo}

Code blocks in Markdown can be created in various ways.

    Indenting content by 4 spaces.
    This will not have any syntax highlighting.


```
Wrapping text with triple backticks also works.
This will have default syntax highlighting (highlighting a few words and "strings").
```

```python
print("And with the triple backticks syntax, you can have syntax highlighting.")
```

```none
print("Or disable all syntax highlighting.")
```

There's a lot of power hidden underneath the triple backticks in MyST Markdown,
as seen in <https://myst-parser.readthedocs.io/en/latest/syntax/roles-and-directives.html>.

+++

Code blocks in reStructuredText can be created in various ways::

    Indenting content by 4 spaces, after a line ends with "::".
    This will have default syntax highlighting (highlighting a few words and "strings").

.. code::

    You can also use the code directive, or an alias: code-block, sourcecode.
    This will have default syntax highlighting (highlighting a few words and "strings").

.. code:: python

    print("And with the directive syntax, you can have syntax highlighting.")

.. code:: none

    print("Or disable all syntax highlighting.")


There's a lot more forms of "blocks" in reStructuredText that can be used, as
seen in https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html#literal-blocks.
````

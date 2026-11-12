"""Regression tests for Celshast's shared copy-button integration."""

import subprocess
import sys
from pathlib import Path

import pytest
from bs4 import BeautifulSoup


def _build(source: Path, output: Path) -> None:
    """Build one fixture in a fresh process, as sphinx-build does in practice."""
    subprocess.run(
        [sys.executable, "-m", "sphinx", "-W", "-b", "html", str(source), str(output)],
        check=True,
        text=True,
        capture_output=True,
    )


@pytest.mark.parametrize("explicit_extension", [False, True])
def test_copybutton_activation_is_explicit(
    tmp_path: Path, explicit_extension: bool
) -> None:
    """Configured projects get copybutton while the theme alone stays safe."""
    source = tmp_path / "source"
    source.mkdir()
    extensions = "['sphinx_copybutton']" if explicit_extension else "[]"
    (source / "conf.py").write_text(
        "project = 'copybutton test'\n"
        f"extensions = {extensions}\n"
        "html_theme = 'celshast'\n"
        + ("copybutton_exclude = '.linenos, .gp'\n" if explicit_extension else ""),
        encoding="utf-8",
    )
    (source / "index.rst").write_text(
        """Copybutton test
===============

.. code-block:: python

   def greet():
       print("hello")


.. code-block:: pycon

   >>> for value in range(2):
   ...     print(value)
   ...
   0
   1

.. code-block:: python
   :linenos:

   first = 1
   second = 2

.. code-block:: text

   final block
""",
        encoding="utf-8",
    )

    output = tmp_path / "output"
    _build(source, output)

    html = (output / "index.html").read_text(encoding="utf-8")
    page = BeautifulSoup(html, "html.parser")
    scripts = [script.get("src", "") for script in page.select("script[src]")]
    styles = [link.get("href", "") for link in page.select("link[rel=stylesheet]")]
    assert any("copybutton.js" in script for script in scripts) is explicit_extension
    assert any("copybutton.css" in style for style in styles) is explicit_extension
    assert len(page.select(".highlight")) == 4
    assert page.select(".highlight .gp")
    assert page.select(".highlight .linenos")
    if explicit_extension:
        script = (output / "_static" / "copybutton.js").read_text(encoding="utf-8")
        assert "let exclude = '.linenos, .gp';" in script
        assert "Undefined" not in script


def test_downstream_copybutton_configuration_is_preserved(tmp_path: Path) -> None:
    """Theme defaults do not replace an explicit downstream configuration."""
    source = tmp_path / "source"
    source.mkdir()
    (source / "conf.py").write_text(
        "project = 'copybutton config test'\n"
        "html_theme = 'celshast'\n"
        "extensions = ['sphinx_copybutton']\n"
        "copybutton_exclude = '.linenos, .gp, .go'\n",
        encoding="utf-8",
    )
    (source / "index.rst").write_text("Test\n====\n", encoding="utf-8")

    output = tmp_path / "output"
    _build(source, output)

    script = (output / "_static" / "copybutton.js").read_text(encoding="utf-8")
    assert "let exclude = '.linenos, .gp, .go';" in script


def test_copybutton_styles_cover_accessibility_and_narrow_layouts() -> None:
    """Shared styles retain focus, contrast, touch size, and code clearance."""
    stylesheet = (
        Path(__file__).parents[1]
        / "src/celshast/assets/styles/extensions/_copybutton.sass"
    ).read_text(encoding="utf-8")

    assert "&:focus-visible" in stylesheet
    assert "outline:" in stylesheet
    assert "height: 2.75rem" in stylesheet
    assert "width: 2.75rem" in stylesheet
    assert "margin-right: 3.75rem" in stylesheet
    assert "var(--color-code-background)" in stylesheet
    assert "var(--color-code-foreground)" in stylesheet
    assert "var(--color-brand-content)" in stylesheet

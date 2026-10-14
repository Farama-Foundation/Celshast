"""Build real Sphinx pages to check footer navigation and metadata switches."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from bs4 import BeautifulSoup


class PageNavigationTests(unittest.TestCase):
    def build(self, builder, pages, root="index", myst=False):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        source = Path(directory.name) / "source"
        output = Path(directory.name) / "output"
        source.mkdir()
        extensions = ["myst_parser"] if myst else []
        (source / "conf.py").write_text(
            f"extensions = {extensions!r}\n"
            'html_theme = "celshast"\n'
            f"root_doc = {root!r}\n",
            encoding="utf-8",
        )
        for name, content in pages.items():
            (source / name).write_text(content, encoding="utf-8")
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "sphinx",
                "-b",
                builder,
                "-W",
                "--keep-going",
                str(source),
                str(output),
            ],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return output

    def links(self, output, builder, docname):
        if builder == "dirhtml" and docname != "index":
            path = output / docname / "index.html"
        else:
            path = output / f"{docname}.html"
        soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
        return {
            direction: soup.select_one(f".related-pages a.{direction}-page")
            for direction in ("prev", "next")
        }

    def test_missing_metadata_at_both_ends(self):
        # Sphinx writes alphabetically: each case renders the page with no
        # metadata before navigation has touched its metadata entry.
        for builder in ("html", "dirhtml"):
            for root, last in (("a_root", "z_last"), ("z_root", "a_last")):
                with self.subTest(builder=builder, root=root):
                    output = self.build(
                        builder,
                        {
                            f"{root}.rst": "Root\n====\n\n.. toctree::\n\n"
                            f"   middle\n   {last}\n",
                            "middle.rst": "Middle\n======\n",
                            f"{last}.rst": "Last\n====\n",
                        },
                        root=root,
                    )
                    first_links = self.links(output, builder, root)
                    self.assertIsNone(first_links["prev"])
                    self.assertIsNotNone(first_links["next"])
                    middle_links = self.links(output, builder, "middle")
                    self.assertIsNotNone(middle_links["prev"])
                    self.assertIsNotNone(middle_links["next"])
                    last_links = self.links(output, builder, last)
                    self.assertIsNotNone(last_links["prev"])
                    self.assertIsNone(last_links["next"])
                    expected = "middle.html" if builder == "html" else "../middle/"
                    self.assertEqual(last_links["prev"]["href"], expected)

    def test_single_page(self):
        for builder in ("html", "dirhtml"):
            with self.subTest(builder=builder):
                output = self.build(builder, {"index.rst": "Home\n====\n"})
                self.assertEqual(
                    self.links(output, builder, "index"), {"prev": None, "next": None}
                )

    def test_empty_navigation_switches(self):
        for builder in ("html", "dirhtml"):
            for suffix in ("rst", "md"):
                with self.subTest(builder=builder, suffix=suffix):
                    pages = {
                        "index.rst": "Home\n====\n\n.. toctree::\n\n"
                        "   first\n   last\n   both\n   end\n",
                        "end.rst": "End\n===\n",
                    }
                    for name, fields in (
                        ("first", ("firstpage",)),
                        ("last", ("lastpage",)),
                        ("both", ("firstpage", "lastpage")),
                    ):
                        if suffix == "rst":
                            content = (
                                "".join(f":{field}:\n" for field in fields)
                                + "\nPage\n====\n"
                            )
                        else:
                            content = (
                                "---\n"
                                + "".join(f"{field}:\n" for field in fields)
                                + "---\n\n# Page\n"
                            )
                        pages[f"{name}.{suffix}"] = content + "\nBody text.\n"
                    output = self.build(builder, pages, myst=suffix == "md")
                    for name, expected in (
                        ("first", {"prev": False, "next": True}),
                        ("last", {"prev": True, "next": False}),
                        ("both", {"prev": False, "next": False}),
                    ):
                        links = self.links(output, builder, name)
                        self.assertEqual(
                            {key: value is not None for key, value in links.items()},
                            expected,
                            name,
                        )


if __name__ == "__main__":
    unittest.main()

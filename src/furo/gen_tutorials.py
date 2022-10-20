import os
from sphinx_gallery import gen_rst
from sphinx_gallery.directives import (
    ImageSg,
    _copy_images,
    depart_imgsg_latex,
    visit_imgsg_latex,
    depart_imgsg_html,
    imgsgnode
)
from sphinx_gallery.gen_gallery import DEFAULT_GALLERY_CONF
from sphinx_gallery.scrapers import matplotlib_scraper


def call_memory(func):
    return 0.0, func()


def generate(source_path, tutorials_path):
    dest_path = tutorials_path
    for filename in os.listdir(tutorials_path):
        if os.path.splitext(filename)[1] != ".py":
            continue

        gen_rst.EXAMPLE_HEADER = ":tutorial: true\n"
        file_path = os.path.join(tutorials_path, filename)

        gallery_config = DEFAULT_GALLERY_CONF
        gallery_config["lang"] = "python"
        gallery_config["src_dir"] = source_path
        gallery_config["titles"] = {}
        gallery_config["titles"][file_path] = ""
        gallery_config["memory_base"] = 0.0
        gallery_config["call_memory"] = call_memory
        gallery_config["min_reported_time"] = float("inf")
        gallery_config["exclude_implicit_doc_regex"] = True
        gallery_config["show_signature"] = False
        gallery_config["filename_pattern"] = ".*"
        gallery_config["reset_modules"] = ()
        gallery_config["image_scrapers"] = tuple([matplotlib_scraper])

        gen_rst.generate_file_rst(filename, dest_path, tutorials_path, gallery_config)


# Copy and paste from sphinx-gallery.directives to fix problem with dirhtml
def visit_imgsg_html(self, node):

    if node["srcset"] is None:
        self.visit_image(node)
        return

    imagedir, srcset = _copy_images(self, node)

    # /doc/examples/subd/plot_1.rst
    docsource = self.document["source"]
    # /doc/
    # make sure to add the trailing slash:
    srctop = os.path.join(self.builder.srcdir, "")
    # examples/subd/plot_1/
    relsource = os.path.relpath(docsource, srctop)
    # /doc/build/html
    desttop = os.path.join(self.builder.outdir, "")
    # /doc/build/html/examples/subd
    dest = os.path.join(desttop, relsource)

    # ../../_images/
    imagerel = os.path.relpath(imagedir, os.path.dirname(dest))
    imagerel = os.path.join("..", imagerel, "")
    if "\\" in imagerel:
        imagerel = imagerel.replace("\\", "/")

    # make srcset str.  Need to change all the prefixes!
    srcsetst = ""
    for mult in srcset:
        nm = os.path.basename(srcset[mult][1:])
        # ../../_images/plot_1_2_0x.png
        relpath = imagerel + nm
        srcsetst += f"{relpath}"
        if mult == 0:
            srcsetst += ", "
        else:
            srcsetst += f" {mult:1.1f}x, "
    # trim trailing comma and space...
    srcsetst = srcsetst[:-2]

    # make uri also be relative...
    nm = os.path.basename(node["uri"][1:])
    uri = imagerel + nm

    alt = node["alt"]
    if node["class"] is not None:
        classst = node["class"][0]
        classst = f'class = "{classst}"'
    else:
        classst = ""

    html_block = f'<img src="{uri}" srcset="{srcsetst}" alt="{alt}"' + f" {classst}/>"
    self.body.append(html_block)


def imagesg_addnode(app):
    app.add_node(
        imgsgnode,
        html=(visit_imgsg_html, depart_imgsg_html),
        latex=(visit_imgsg_latex, depart_imgsg_latex),
    )


def setup(app):
    """Setup extension"""
    app.add_directive("image-sg", ImageSg)

    imagesg_addnode(app)

    metadata = {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
        "version": "0.0.1",
    }
    return metadata

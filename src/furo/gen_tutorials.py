import os
from sphinx_gallery import gen_rst
from sphinx_gallery.gen_gallery import DEFAULT_GALLERY_CONF

def generate(source_path):
    dest_path = source_path
    for filename in os.listdir(source_path):
        if os.path.splitext(filename)[1] != ".py":
            continue

        gen_rst.EXAMPLE_HEADER = ":tutorial: true\n"

        file_path = os.path.join(source_path, filename)
        gallery_config = DEFAULT_GALLERY_CONF
        gallery_config["lang"] = "python"
        gallery_config["src_dir"] = file_path
        gallery_config["titles"] = {}
        gallery_config["titles"][file_path] = ""
        gallery_config["memory_base"] = 0.0
        gallery_config["min_reported_time"] = float("inf")
        gallery_config["exclude_implicit_doc_regex"] = True
        gallery_config["show_signature"] = False

        gen_rst.generate_file_rst(filename, dest_path, source_path, gallery_config)

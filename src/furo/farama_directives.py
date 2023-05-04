"""Sphinx Extensions used by Farama's projects.
"""

from docutils import nodes
from docutils.statemachine import StringList
from docutils.parsers.rst.directives import images
from docutils.parsers.rst import Directive, directives


class FaramaProjectLogoDirective(images.Figure):
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        "alt": directives.unchanged,
        "height": directives.length_or_unitless,
        "width": directives.length_or_percentage_or_unitless,
        "class": directives.class_option,
    }

    def run(self):
        (img_node,) = images.Figure.run(self)
        # Add custom class to the image node.
        img_node.attributes["classes"].append("farama-project-logo")
        return [img_node]


class FaramaProjectHeadingDirective(Directive):
    has_content = True

    def run(self):
        self.assert_has_content()

        container = nodes.container()

        html_content = []
        html_content.append("<h2 class='farama-project-heading'>")
        html_content.append(self.content[0])
        html_content.append("</h2>")
        html_content = StringList(html_content)

        self.state.nested_parse(html_content, 0, container)
        return [container]

from jinja2 import Environment, FileSystemLoader

from application.settings import TEMPLATES_DIR


class View:
    def __init__(self, template_name: str, context=None):
        if context is None:
            context = {}
        self.template_name = template_name
        self.context = context

    def render(self) -> str:
        template_env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
        template = template_env.get_template(self.template_name)
        content = template.render(self.context)

        return content

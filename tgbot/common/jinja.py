import re
from typing import Any

from jinja2 import Environment, FileSystemLoader

from .types import PathType
from .utils.functions import get_now


def render_template(template_name: str,
                    templates_dir: PathType,
                    data: dict | None = None) -> str:
    if data is None:
        context = {}
    else:
        context = data.copy()
    context.update(get_context())

    env = Environment(
        loader=FileSystemLoader(searchpath=templates_dir),
        trim_blocks=True,
        lstrip_blocks=True,
        autoescape=True
    )

    template = env.get_template(template_name)
    rendered = template.render(**context)
    rendered = rendered.replace("\n", " ")
    rendered = rendered.replace("<br>", "\n")
    rendered = re.sub(" +", " ", rendered).replace(" .", ".").replace(" ,", ",")
    rendered = "\n".join(line.strip() for line in rendered.split("\n"))

    return rendered


def get_context() -> dict[str, Any]:
    return {
        "now": get_now(),
    }

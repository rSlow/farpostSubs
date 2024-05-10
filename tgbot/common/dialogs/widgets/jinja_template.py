from typing import Optional

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.text import Text

from common import jinja
from common.jinja import PathType


class JinjaTemplate(Text):
    def __init__(self,
                 template_name: str,
                 templates_dir: PathType,
                 template_data: Optional[dict] = None,
                 when: WhenCondition = None):
        super().__init__(when=when)
        self._template_name = template_name
        self._templates_dir = templates_dir
        if template_data is None:
            self._template_data = {}
        else:
            self._template_data = template_data

    async def _render_text(self,
                           data: dict,
                           manager: DialogManager) -> str:
        template_data = self._template_data.copy()
        template_data.update(data)
        rendered = jinja.render_template(
            template_name=self._template_name,
            templates_dir=self._templates_dir,
            data=template_data
        )
        return rendered

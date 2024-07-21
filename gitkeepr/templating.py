import logging
import os
import shutil
from typing import Dict, List

from jinja2 import Environment, FileSystemLoader

logger = logging.getLogger(__name__)


class TemplateManager:
    """Template engine for repositories."""

    templated_files: List[str] = [
        "README.md",
        ".github/PULL_REQUEST_TEMPLATE.md",
    ]

    def __init__(self, template_dir: str):
        self.template_dir = template_dir
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            trim_blocks=False,
            lstrip_blocks=False,
        )

    def render_template(self, template_file: str, context: Dict[str, str]) -> str:
        """Render a template file with the given context."""
        template = self.env.get_template(template_file)
        return template.render(context)

    def create(self, base_dir: str, context: Dict[str, str]) -> None:
        """Generate files based on templates and context."""
        logger.debug(f"Generating files from '{self.template_dir}'")
        for file in self.templated_files:
            target_path = os.path.join(base_dir, file)
            template_file = os.path.join(self.template_dir, file)
            logger.debug(f"Generating '{file}' from template {template_file}")
            rendered_content = self.render_template(f"{file}.j2", context)
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            with open(target_path, "w") as f:
                f.write(rendered_content)
            logger.debug(f"Wrote '{file}' to '{base_dir}'")
        logger.info(f"Generated {len(self.templated_files)} files in '{base_dir}'")

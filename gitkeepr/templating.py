import logging
import os
import shutil
from typing import Dict, List

from jinja2 import Environment, FileSystemLoader

logger = logging.getLogger(__name__)


class TemplateManager:
    """Template engine for repositories."""

    basic_templated_files: List[str] = [
        "README.md",
        ".github/PULL_REQUEST_TEMPLATE.md",
    ]
    additional_templated_files = [".pre-commit-config.yaml", ".gitignore"]

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
        rendered_content = template.render(context)
        if not rendered_content.endswith("\n"):
            rendered_content += "\n"
        return rendered_content

    def generate_files(self, base_dir: str, files: List[str], context: Dict[str, str]):
        for file in files:
            target_path = os.path.join(base_dir, file)
            template_file = os.path.join(self.template_dir, file)
            logger.debug(f"Generating '{file}' from template {template_file}")
            rendered_content = self.render_template(f"{file}.j2", context)
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            with open(target_path, "w") as f:
                f.write(rendered_content)
            logger.debug(f"Wrote '{file}' to '{base_dir}'")

    def create(self, base_dir: str, context: Dict[str, str], minimal: bool) -> None:
        """Generate files based on templates and context."""
        files_templated_count = 0
        logger.info(f"Generating files from '{self.template_dir}'")
        self.generate_files(base_dir, self.basic_templated_files, context)
        files_templated_count += len(self.basic_templated_files)
        if not minimal:
            logger.info(f"Generating additional repo files")
            self.generate_files(base_dir, self.additional_templated_files, context)
            files_templated_count += len(self.additional_templated_files)
        logger.info(f"Generated {files_templated_count} files in '{base_dir}'")

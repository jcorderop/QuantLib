"""
Created: 22.05.2023
Description:
    * This Library offers common functionality used to convert the readme.md file to html.
"""
__author__ = "OE - JC"
from app.util.config.ProjectSpecifics import *
__version__ = API_VERSION
__license__ = LICENSE

# Import modules
from markdown_it import MarkdownIt
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.footnote import footnote_plugin
from pathlib import Path
from app.util.CommonApiUtil import get_readme_mb_path, get_index_file_path, get_index_template_path

import logging
logger = logging.getLogger(__name__)


def _build_index_html(html_text) -> str:
    index = Path(get_index_template_path()).read_text(encoding="utf-8")
    return index.replace('README', html_text)


def _transform_readme_md_to_html() -> str:
    md = (
        MarkdownIt('commonmark', {'breaks': True, 'html': True})
        .use(front_matter_plugin)
        .use(footnote_plugin)
        .enable('table')
    )
    text = Path(get_readme_mb_path()).read_text(encoding="utf-8")
    return md.render(text)


def build_root_web() -> None:
    logger.info('Creating root index.html from readme.md')
    html_text = _transform_readme_md_to_html()
    index_html = _build_index_html(html_text)
    index_file_path = get_index_file_path()
    Path(index_file_path).write_text(index_html, encoding='utf-8')



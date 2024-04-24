from typing import Optional
from view.config import MAIN_PAGE

def __load_page(template_path: str, formating: Optional[dict] = None):
    with open(template_path, 'r') as template:
        page = template.read()
    if formating:
        page = page.format(**formating)
    return page

def main_page():
    return __load_page(MAIN_PAGE)

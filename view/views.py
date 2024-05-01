from typing import Optional
import view.config as config
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader(config.VIEW_TEMPLATES))

def __load_page(template_path: str, formating: Optional[dict] = None):
    with open(template_path, 'r') as template:
        page = template.read()
    if formating:
        page = page.format(**formating)
    return page

def main_page():
    return __load_page(config.MAIN_PAGE)

def films(films_data: list):

    template = env.get_template(config.FILMS)

    return template.render(films=films_data)

def actors(actors_data: list):

    template = env.get_template(config.ACTORS)

    return template.render(actors=actors_data)
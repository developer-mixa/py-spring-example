"""Module with all views for the site."""


from typing import Optional

from jinja2 import Environment, FileSystemLoader

import view.config as config

env = Environment(loader=FileSystemLoader(config.VIEW_TEMPLATES))


def __load_page(template_path: str, formating: Optional[dict] = None):
    with open(template_path, 'r') as template:
        page = template.read()
    if formating:
        page = page.format(**formating)
    return page


def main_page() -> str:
    """Present main page of the site.

    Returns:
        str: html-format of main page
    """
    return __load_page(config.MAIN_PAGE)


def films(_, films_data: list) -> str:
    """Html file with actors view.

    Args:
        _: Controller
        films_data (list): list of films

    Returns:
        str: htpl-format of films
    """
    template = env.get_template(config.FILMS)

    return template.render(films=films_data)


def actors(_, actors_data: list) -> str:
    """Html file with actors view.

    Args:
        _: Controller
        actors_data (list): list of actors

    Returns:
        str: htpl-format of actors
    """
    template = env.get_template(config.ACTORS)

    return template.render(actors=actors_data)

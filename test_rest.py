"""Module for testing rest api."""


import json
import multiprocessing

import pytest
import requests

from controller.actor_controller import ActorController
from controller.film_controller import FilmController
from controller.utils.responses import CREATED, OK
from controller.utils.rest_controller import GlobalRestController

PORT = 8080

app = GlobalRestController('localhost', PORT, controllers=[FilmController(), ActorController()])

INDEX = 'http://127.0.0.1:8080/'
FILMS = f'{INDEX}films'
ACTORS = f'{INDEX}actors'

TEST_GET_DATA = (INDEX, FILMS, ACTORS)

films_data = {
    'name': 'Test film',
    'description': 'Test description',
    'rating': 5.0,
}

actors_data = {
    'name': 'Test',
    'surname': 'Testov',
    'age': 18,
}

TEST_POST_PUT_DELETE_DATA = (
    (FILMS, films_data),
    (ACTORS, actors_data),
)


@pytest.mark.parametrize('url', TEST_GET_DATA)
def test_get(url: str):
    """Test working get queries.

    Args:
        url (str): url for the get query
    """
    print(app)
    process = multiprocessing.Process(target=app.run)
    process.start()

    response = requests.get(url)
    assert response.status_code == OK

    process.terminate()
    process.join()


@pytest.mark.parametrize('model_url, model_data', TEST_POST_PUT_DELETE_DATA)
def test_post_put_delete(model_url: str, model_data: dict):
    """Test that the post put delete methods return successful values.

    Args:
        model_url (str): url for the required model
        model_data (dict): data for our model
    """
    process = multiprocessing.Process(target=app.run)
    process.start()

    create_url = f'{model_url}/create/'
    response = requests.post(create_url, data=json.dumps(model_data))

    assert response.status_code == CREATED

    model_data['id'] = response.content.decode()
    update_url = f'{model_url}/update/'
    response = requests.put(update_url, data=json.dumps(model_data))

    assert response.status_code == OK

    delete_film_data = {
        'id': model_data['id'],
    }

    delete_url = f'{model_url}/delete/'

    response = requests.delete(delete_url, data=json.dumps(delete_film_data))

    process.terminate()
    process.join()

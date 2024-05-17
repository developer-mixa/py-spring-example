"""Module for working with db entities."""
import os

import dotenv
from sqlalchemy import Engine
from sqlalchemy import create_engine as create_engine_sql

PG_VARS = 'POSTGRES_USER', 'POSTGRES_PASSWORD', 'POSTGRES_HOST', 'PG_PORT', 'POSTGRES_DB'
DB_URL = 'postgresql+psycopg://'


def __get_db_url() -> str:
    """Get database depend on evv file.

    Returns:
        str: database url
    """
    dotenv.load_dotenv()
    credentials = [os.environ.get(pg_var) for pg_var in PG_VARS]
    credentials[2] = os.getenv('POSTGRES_HOST') if os.getenv('DEBUG_MODE') == 'false' else 'localhost'
    return DB_URL + '{0}:{1}@{2}:{3}/{4}'.format(*credentials)


def create_engine() -> Engine:
    """Generate engine which everyone uses.

    Returns:
        Engine: our database engine
    """
    return create_engine_sql(__get_db_url())

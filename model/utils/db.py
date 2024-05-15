"""Module for working with db entities."""
import os

import dotenv
from sqlalchemy import Engine
from sqlalchemy import create_engine as create_engine_sql

PG_VARS = 'PG_HOST', 'PG_PORT', 'PG_USER', 'PG_PASSWORD', 'PG_DBNAME'
DB_URL = 'postgresql+psycopg://'


def __get_db_url() -> str:
    """Get database depend on evv file.

    Returns:
        str: database url
    """
    dotenv.load_dotenv()
    credentials = {pg_var: os.environ.get(pg_var) for pg_var in PG_VARS}
    return DB_URL + '{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DBNAME}'.format(**credentials)


def create_engine() -> Engine:
    """Generate engine which everyone uses.

    Returns:
        Engine: our database engine
    """
    return create_engine_sql(__get_db_url())

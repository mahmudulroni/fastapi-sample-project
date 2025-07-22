# If you need default root user then run this file
# python -m app.initial_data
# This file is used to create initial user data in the database

import logging

from sqlmodel import Session

from app.core.database import engine, init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    with Session(engine) as session:
        init_db(session)


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()

"""
The file that holds the logic to 
initialize and connect to the database.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import logging

# Setup logging out to a file
db_log_file_name = 'db.log'
db_handler_log_level = logging.INFO
db_logger_log_level = logging.DEBUG

db_handler = logging.FileHandler(db_log_file_name)
db_handler.setLevel(db_handler_log_level)

db_logger = logging.getLogger('sqlalchemy')
db_logger.addHandler(db_handler)
db_logger.setLevel(db_logger_log_level)

# Creates the engine to connect with our database
# TODO: Change the name from "vet" to something relevant
engine = create_engine("sqlite:///nba.db", echo=False)

# A Scoped Session helps us when creating our apps
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

# Base is the class we will extend
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import models
    Base.metadata.create_all(bind=engine)
    if db_session.query(models.Team).count() == 0:
        Celtics = models.Team("Celtics", 5)
        db_session.add(Celtics)
        Hawks = models.Team("Hawks", 2)
        db_session.add(Hawks)
        Nuggets = models.Team("Nuggets", 2)
        db_session.add(Nuggets)
        Pacers = models.Team("Pacers", 2)
        db_session.add(Pacers)
        Pistons = models.Team("Pistons", 2)
        db_session.add(Pistons)
        Raptors = models.Team("Raptors", 2)
        db_session.add(Raptors)
        db_session.commit()

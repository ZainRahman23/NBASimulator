"""
The file that holds the schema/classes
that will be used to create objects
and connect to data tables.
"""

from sqlalchemy import ForeignKey, Column, INTEGER, TEXT
from sqlalchemy.orm import relationship
from database import Base

# TODO: Complete your models

class User(Base):
    __tablename__ = "users"

    # Columns
    id = Column("id", INTEGER, primary_key=True)
    username = Column("username", TEXT, nullable=False)
    password = Column("password", TEXT, nullable=False)
    team_id = Column("team_id", INTEGER, ForeignKey("teams.id"), nullable=True)

    results = relationship("Result", back_populates="user")
    team = relationship("Team", back_populates="users")
    # Constructor
    def __init__(self, username, password):
        # id auto-increments
        self.username = username
        self.password = password

    def __repr__(self):
        return self.username
class Team(Base):
    __tablename__ = "teams"

    # Columns
    id = Column("id", INTEGER, primary_key=True)
    team_name = Column("team_name", TEXT, nullable=False)
    rating = Column("rating", INTEGER, nullable=False)

    results = relationship("Result", back_populates="team")
    users = relationship("User", back_populates="team")
    # Constructor
    def __init__(self, team_name, rating):
        # id auto-increments
        self.team_name = team_name
        self.rating = rating

    def __repr__(self):
        return self.team_name

class Result(Base):
    __tablename__ = "results"

    # Columns
    id = Column("id", INTEGER, primary_key=True)
    team_id = Column("team_id", INTEGER, ForeignKey("teams.id"), nullable=False)
    user_id = Column("user_id", INTEGER, ForeignKey("users.id"), nullable=False)
    wins = Column("wins", INTEGER, nullable=False)
    losses = Column("losses", INTEGER, nullable=False)
    points = Column("points", INTEGER, nullable=False)
    played = Column("played", INTEGER, nullable=False)

    user = relationship("User", back_populates="results")
    team = relationship("Team", back_populates="results")

    # Constructor
    def __init__(self, team_id, user_id, wins, losses, played):
        # id auto-increments
        self.team_id = team_id
        self.user_id = user_id
        self.wins = wins
        self.losses = losses
        self.points = wins - losses
        self.played = played

    def __repr__(self):
        return self.team_id
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Course(Base):
    __tablename__ = 'course'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(String(10), primary_key=True)
    name = Column(String(140), nullable=False)
    description = Column(String(1000))
    date = Column(String(30))
    period = Column(String(5))
    credit = Column(String(5))
    rating = Column(Float())
    ratings = Column(Integer(), default=3)

    def __init__(self, id, name, desc, date, period, credit):
        self.id = id
        self.name = name
        self.desc = desc
        self.date = date
        self.period = period
        self.credit = credit
        self.rating = 3.0
        self.ratings = 0

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    course = Column(String(10), ForeignKey('course.id'))
    body = Column(String(1000))
    iteration = Column(String(10))
    rating = Column(Integer, nullable=True)

    def __init__(self, course, body, iteration, rating):
        self.course = course
        self.body = body
        self.iteration = iteration
        self.rating = rating

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(16))
    password_hash = Column(String(64))
    role = Column(Integer, nullable=True)
    token = Column(String(64))
    expires = Column(Integer)

    def __init__(self, username, password_hash, role):
        self.username = username
        self.password_hash = password_hash
        self.role = role
        self.token = ''
        self.expires = 0


# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///scivoo_sqlalchemy.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)

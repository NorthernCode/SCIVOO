import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
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

    def __init__(self, id, name, desc, date, period):
        self.id = id
        self.name = name
        self.desc = desc
        self.date = date
        self.period = period

class Comment(Base):
    __tablename__ = 'comment'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
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

class WaitingComment(Base):
    __tablename__ = 'waiting_comment'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    course = Column(String(10), ForeignKey('course.id'))
    header = Column(String(50))
    body = Column(String(1000))
    iteration = Column(String(10))
    rating = Column(Integer)

    def __init__(self, course, body, iteration, rating):
        self.course = course
        self.body = body
        self.iteration = iteration
        self.rating = rating

# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///scivoo_sqlalchemy.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)

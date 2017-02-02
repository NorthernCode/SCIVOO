from sqlalchemy_decl import Course, Comment, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///scivoo_sqlalchemy.db')
Base.metadata.bind = engine

DBSession = sessionmaker()
DBSession.bind = engine
db = DBSession()

f_courses = open('course_data.csv', 'r', encoding='utf-8')

for course in f_courses:
    data = course.split(';')
    if(data[1] == '' or data[2] == ''):
        continue
    check = db.query(Course).filter(Course.id.like(data[1])).all()
    if(len(check) > 0):
        continue
    if(len(data) < 6):
        item = Course(data[1], data[2], '', '', '')
    else:
        item = Course(data[1], data[2], '', data[5], '')
    db.add(item)

db.commit()

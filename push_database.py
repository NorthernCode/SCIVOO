from sqlalchemy_decl import Course, Comment, Base, User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import re

engine = create_engine('sqlite:///scivoo_sqlalchemy.db')
Base.metadata.bind = engine

DBSession = sessionmaker()
DBSession.bind = engine
db = DBSession()

#Courses

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

#Admin User
admin = db.query(User).filter(User.username.like('admin')).all() #Should return empty set
if(len(admin) == 0):
	item = User('admin', '01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b', 0)
	db.add(item)

db.commit()


def parsePeriod(periods):
    result = ''
    periods = periods.replace('¿', '-')
    for char in periods:
        if(char == 'I' or char == 'V' or char == ',' or char == '-'):
            result += char
        elif(char == ' ' ):
            continue
        else:
            return parseRomans(result.strip())
    return parseRomans(result.strip())

def parseRomans(periods):
    result = periods.replace('III', '3')
    result = result.replace('II', '2')
    result = result.replace('IV', '4')
    result = result.replace('I', '1')
    result = result.replace('V', '5')
    return result

def getStartingPeriods(periods):
    result = ''
    starts = True
    for char in periods:
        if(char == ','):
            starts = True
            result += char
        elif(char == '-'):
            starts = False
        elif(starts):
            result += char
    return result

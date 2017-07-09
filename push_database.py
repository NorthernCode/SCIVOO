from sqlalchemy_decl import Course, Comment, Base, User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import re


def parseRomans(periods):
    result = periods.replace('III', '3')
    result = result.replace('II', '2')
    result = result.replace('IV', '4')
    result = result.replace('I', '1')
    result = result.replace('V', '5')
    return result

def parsePeriod(periods):
    result = ''
    #periods = periods.replace('¿', '-')
    for char in periods:
        if(char == 'I' or char == 'V' or char == ',' or char == '-'):
            result += char
        elif(char == ' ' ):
            continue
        else:
            return parseRomans(result.strip())
    return parseRomans(result.strip())

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
    if(len(data) < 10):
        item = Course(data[1], data[2], '', '', '', '', '')
    else:
        item = Course(data[1], data[2], data[8], data[9], data[5], parsePeriod(data[6]), data[7])
    db.add(item)

#Admin User
admin = db.query(User).filter(User.username.like('admin')).all() #Should return empty set
if(len(admin) == 0):
	item = User('admin', '81729e25011a4162746868bc75e52b954d40b8581c9b892cd2e0de63acc8d8c3', 0)
	db.add(item)

db.commit()

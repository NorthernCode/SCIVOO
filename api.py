import os
import json
from lib.bottle import get, post, request, run, static_file
from sqlalchemy_decl import Course, Comment, WaitingComment, Base
from sqlalchemy import create_engine, or_, and_
from sqlalchemy.orm import sessionmaker

path = os.getcwd()

engine = create_engine('sqlite:///scivoo_sqlalchemy.db')
Base.metadata.bind = engine

DBSession = sessionmaker()
DBSession.bind = engine
db = DBSession()

@get('/')
def default():
    return "Default"

@post('/search')
def search():
    if (request.forms.get('search') && request.forms.get('period')):
        searchString = '%' + request.forms.get('search') + '%'
        periodString = '%' + request.forms.get('period') + '%'
        data = db.query(Course).filter(and_(or_(Course.id.like(searchString), Course.name.like(searchString)), Course.period.like(periodString))).all()
        result = []
        for row in data:
            item = {}
            item['id'] = row.id
            item['name'] = row.name
            item['description'] = row.description
            result.append(item)

        return {'search':request.forms.get('search'), 'period':request.forms.get('period'), 'courses':result}
    else:
        return {'search':'', 'courses':[]}

@post('/comment/<id>')
def add_comment():
    return "jee"

@get('/static/<filepath>')
def get_static(filepath):
    return static_file(filepath, root=(path + '/static'))

run(host='localhost', port=8080, debug=True)

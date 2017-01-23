import os
import json
from lib.bottle import get, post, request, run, static_file
from sqlalchemy_decl import Course, Comment, WaitingComment, Base
from sqlalchemy import create_engine
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

@get('/search')
def search():
    if (request.forms.get('search')):
        searchString = '%' + request.forms.get('search') + '%'
        data = db.query(Course).filter(or_(Course.id.like(searchString), Course.name.like(searchString))).all()
        result = []
        for row in data:
            item = {}
            item['id'] = row.id
            item['name'] = row.name
            item['description'] = row.description
            result.append(item)

        return {'search':request.forms.get('search'), 'courses':result}
    else:
        return {'search':'', 'courses':[]}

@post('/comment/<id>')
def add_comment():
    return "jee"

@get('/static/<filepath>')
def get_static(filepath):
    return static_file(filepath, root=(path + '/static'))

run(host='localhost', port=8080, debug=True)

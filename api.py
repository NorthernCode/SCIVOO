import os
import json
from lib.bottle import get, post, request, route, run, static_file
from sqlalchemy_decl import Course, Comment, Base
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
    return static_file('index.html', root=(path + '/static-build'))

@route('<any:path>', 'OPTIONS')
def options_call(any):
    return {}

@get('/api/course/<id>')
def course_info(id):
    data = db.query(Course).filter(Course.id.like(id)).all()
    comment_data = db.query(Comments).filter(Comments.course.like(data[0].id)).all()
    item = {}
    item['id'] = data[0].id
    item['name'] = data[0].name
    item['description'] = data[0].description
    item['period'] = data[0].period
    comments = []
    for row in comment_data:
        comment_item = {}
        comment_item['name'] = row.body
        comment_item['description'] = row.iteration
        comment_item['description'] = row.rating
        comments.append(comment_item)
    item['comments'] = comments



    return item

@post('/api/search')
def search():
    if (request.forms.get('search') and request.forms.get('period')):
        searchString = '%' + request.forms.get('search') + '%'
        periodString = '%' + request.forms.get('period') + '%'
        if(request.forms.get('period') == 'Any'):
            data = db.query(Course).filter(or_(Course.id.like(searchString), Course.name.like(searchString))).all()
        else:
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

@post('/api/comment/<id>')
def add_comment(id):
    if (request.forms.get('body') and request.forms.get('iteration') and request.forms.get('rating')):
        comment = Comment(id, request.forms.get('body'), request.forms.get('iteration'), request.forms.get('rating'))
        db.add(comment)
        db.commit()

@get('/static/<filepath:path>')
def get_static(filepath):
    return static_file(filepath, root=(path + '/static'))

run(host='localhost', port=8080, debug=True)

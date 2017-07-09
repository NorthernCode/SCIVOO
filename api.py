#!/usr/bin/env python
import os, json, hashlib, math, time
from bottle import get, post, request, route, run, static_file
from sqlalchemy_decl import Course, Comment, Base, User
from sqlalchemy import create_engine, or_, and_, update
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

#@get('/course/<any:path>')
#def default_course(any):
#    return static_file('index.html', root=(path + '/static-build'))

#@route('<any:path>', 'OPTIONS')
#def options_call(any):
#    return {}

@get('/course/<id>')
def course_info(id):
    data = db.query(Course).filter(Course.id.like(id)).all()
    comment_data = db.query(Comment).filter(Comment.course.like(data[0].id)).all()
    item = {}
    item['id'] = data[0].id
    item['name'] = data[0].name
    item['description'] = data[0].description
    item['period'] = data[0].period
    item['credit'] = data[0].credit
    item['rating'] = data[0].rating
    item['workload'] = data[0].workload
    comments = []
    for row in comment_data:
        comment_item = {}
        comment_item['body'] = row.body
        comment_item['iteration'] = row.iteration
        comment_item['rating'] = row.rating
        comment_item['workload'] = row.workload
        comments.append(comment_item)
    item['comments'] = comments

    return item

@post('/search')
def search():
    if (request.forms.get('search') and request.forms.get('period') and request.forms.get('credit')):
        searchString = '%' + request.forms.get('search') + '%'
        periodString = '%' + request.forms.get('period') + '%'
        creditString = '%' + request.forms.get('credit') + '%'
        if(request.forms.get('period') == 'Any'):
            data = db.query(Course).filter(or_(Course.id.like(searchString), Course.name.like(searchString))).all()
        else:
            if(request.forms.get('search') == ''):
                data = db.query(Course).filter(Course.period.like(periodString)).all()
            else:
                data = db.query(Course).filter(and_(or_(Course.id.like(searchString), Course.name.like(searchString)), Course.period.like(periodString))).all()
        result = []
        for row in data:
            item = {}
            item['id'] = row.id
            item['name'] = row.name
            item['description'] = row.description
            item['period'] = row.period
            item['credit'] = row.credit
            item['rating'] = row.rating
            result.append(item)

        return {'search':request.forms.get('search'), 'period':request.forms.get('period'), 'courses':result}
    else:
        return {'search':'', 'courses':[]}

@post('/comment/<id>')
def add_comment(id):
    if (request.forms.get('body') and request.forms.get('iteration') and request.forms.get('rating') and request.forms.get('workload')):
        course_item = db.query(Course).filter(Course.id == id).first()

        new_rating = (float(request.forms.get('rating')) + course_item.rating * course_item.ratings) / (course_item.ratings + 1)
        course_item.rating = new_rating

        new_workload = (float(request.forms.get('workload')) + course_item.workload * course_item.ratings) / (course_item.ratings + 1)
        course_item.workload = new_workload

        course_item.ratings = course_item.ratings + 1

        comment = Comment(id, request.forms.get('body'), request.forms.get('iteration'), request.forms.get('rating'), request.forms.get('workload'))
        db.add(comment)
        db.commit()

    comment_data = db.query(Comment).filter(Comment.course == id).all()
    comments = []
    for row in comment_data:
        comment_item = {}
        comment_item['body'] = row.body
        comment_item['iteration'] = row.iteration
        comment_item['rating'] = row.rating
        comment_item['workload'] = row.workload
        comments.append(comment_item)

    return {'comments':comments}

@post('/login')
def login():
    if (request.forms.get('username') and request.forms.get('password')):
        password_hash = hashlib.sha256(str.encode(request.forms.get('password'))).hexdigest()
        user = db.query(User).filter(and_(User.username.like(request.forms.get('username')), User.password_hash.like(password_hash))).first()
        if(user):
            user.token = '123'
            user.expires = math.floor(time.time()) + 1800
            db.commit()
            return {'token':'123'}
    return {'token':'', 'message':'login failed'}

@post('/isadmin')
def is_admin():
    if (request.forms.get('token')):
        user = db.query(User).filter(User.token.like(request.forms.get('token'))).first()
        if (user):
            if (user.expires > math.floor(time.time())):
                return {'success':'true'}
    return {}

@get('/static/<filepath:path>')
def get_static(filepath):
    return static_file(filepath, root=(path + '/static'))

#run(host='localhost', port=8080, debug=True)
run(server='cgi', debug=True)

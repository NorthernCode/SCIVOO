#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os, json, hashlib, math, time, uuid
sys.path.append('lib')
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

def is_admin(request):
    if (request.forms.get('token')):
        user = db.query(User).filter(User.token.like(request.forms.get('token'))).first()
        if (user):
            if (user.expires > math.floor(time.time())):
                user.expires = math.floor(time.time()) + 600
                db.commit()
                return True
    return False

@get('/')
def default():
    return static_file('index.html', root=(path + '/static-build'))

@get('/course/<id>')
def course_info(id):
    data = db.query(Course).filter(Course.id.like(id)).all()
    comment_data = db.query(Comment).filter(and_(Comment.course == data[0].id, Comment.removed == False)).all()
    item = {}
    item['id'] = data[0].id
    item['name'] = data[0].name
    item['desc_outcome'] = data[0].desc_outcome
    item['desc_content'] = data[0].desc_content
    item['period'] = data[0].period
    item['credit'] = data[0].credit
    item['rating'] = data[0].rating
    item['workload'] = data[0].workload
    comments = []
    for row in comment_data:
        comment_item = {}
        comment_item['id'] = row.id
        comment_item['body'] = row.body
        comment_item['iteration'] = row.iteration
        comment_item['rating'] = row.rating
        comment_item['workload'] = row.workload
        comments.append(comment_item)
    item['comments'] = comments

    return item

@post('/search')
def search():
    if(request.forms.get('search') or request.forms.get('period') != 'Any' or request.forms.get('credit') != 'Any'):
        searchString = '%' + request.forms.get('search') + '%'
        periodString = '%' + request.forms.get('period') + '%'
        creditString = '%' + request.forms.get('credit') + '%'
        startFrom = 0
        sortBy = "name"

        if(request.forms.get('offset')):
            startFrom = int(request.forms.get('offset'))

        if(request.forms.get('sort')):
            sortBy = int(request.forms.get('sort'))

        if(request.forms.get('period') == 'Any'):
            if(request.forms.get('credit') == 'Any'):
                data = db.query(Course).filter(or_(Course.id.like(searchString), Course.name.like(searchString))).order_by(sortBy).limit(50).offset(startFrom).all() #Only Name
            else:
                data = db.query(Course).filter(and_(or_(Course.id.like(searchString), Course.name.like(searchString)), Course.credit.like(creditString))).order_by(sortBy).limit(50).offset(startFrom).all() #Credit and Name
        else:
            if(request.forms.get('search') == ''):
                if(request.forms.get('credit') == 'Any'):
                    data = db.query(Course).filter(Course.period.like(periodString)).order_by(sortBy).limit(50).offset(startFrom).all() #Only Period
                else:
                    data = db.query(Course).filter(and_(Course.period.like(periodString), Course.credit.like(creditString))).order_by(sortBy).limit(50).offset(startFrom).all() #Period and Credit
            else:
                if(request.forms.get('credit') == 'Any'):
                    data = db.query(Course).filter(and_(or_(Course.id.like(searchString), Course.name.like(searchString)), Course.period.like(periodString))).order_by(sortBy).limit(50).offset(startFrom).all() #Period and Name
                else:
                    data = db.query(Course).filter(and_(and_(or_(Course.id.like(searchString), Course.name.like(searchString)), Course.period.like(periodString)), Course.credit.like(creditString))).order_by(sortBy).limit(50).offset(startFrom).all() #All fields
        result = []
        for row in data:
            item = {}
            item['id'] = row.id
            item['name'] = row.name
            item['period'] = row.period
            item['credit'] = row.credit
            item['rating'] = row.rating
            item['workload'] = row.workload
            result.append(item)

        return {'search':request.forms.get('search'), 'period':request.forms.get('period'), 'courses':result}
    else:
	return {'search':"", 'courses':[]}

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

    comment_data = db.query(Comment).filter(and_(Comment.course == id, Comment.removed == False)).all()
    comments = []
    for row in comment_data:
        comment_item = {}
        comment_item['id'] = row.id
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
        user = db.query(User).filter(and_(User.username == request.forms.get('username'), User.password_hash == password_hash)).first()
        if(user):
            if (user.expires > math.floor(time.time())):
                return {'token': user.token}
            token = uuid.uuid4().hex + uuid.uuid4().hex
            user.token = token
            user.expires = math.floor(time.time()) + 600
            db.commit()
            return {'token': token}
    return {'token':'', 'message':'login failed'}

@post('/isadmin')
def check_admin():
    if (is_admin(request)):
        return {'success':'true'}
    return {}

@post('/comment/remove/<id>')
def remove_comment(id):
    if (is_admin(request)):
        comment = db.query(Comment).filter(Comment.id == id).all()
        comment[0].removed = True
        db.commit()

        course_id = comment[0].course
        comment_data = db.query(Comment).filter(and_(Comment.course == course_id, Comment.removed == False)).all()
        comments = []
        for row in comment_data:
            comment_item = {}
            comment_item['id'] = row.id
            comment_item['body'] = row.body
            comment_item['iteration'] = row.iteration
            comment_item['rating'] = row.rating
            comment_item['workload'] = row.workload
            comments.append(comment_item)

        return {'comments':comments}
    return {}

@get('/static/<filepath:path>')
def get_static(filepath):
    return static_file(filepath, root=(path + '/static'))

#run(host='localhost', port=8080, debug=True) #dynamic server
run(server='cgi', debug=False)

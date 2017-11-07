#!/usr/bin/env python
import sys, os, json, hashlib, math, time, uuid
sys.path.append('lib')
from bottle import get, post, request, route, run, static_file
from sqlalchemy_decl import Course, Comment, Base, User
from sqlalchemy import create_engine, or_, and_, update


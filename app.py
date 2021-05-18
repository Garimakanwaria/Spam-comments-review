# app.py
# Required Imports
import os
# from textblob import Textblob
from flask_cors import cross_origin
from flask import request, jsonify
from functions import *
from urllib.request import urlopen

from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app

# Initialize Flask App
app = Flask(__name__)
# Initialize Firestore DB


cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()
todo_ref = db.collection('comments')


@app.route('/find_city', methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def fc():
    query_parameters = request.args
    ip = query_parameters.get('ip')
    with urlopen('https://ipapi.co/' + ip + '/json') as r:
        text = r.read()

    return text


@app.route('/list', methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def read():
    all_todos = [doc.to_dict() for doc in todo_ref.stream()]
    print(all_todos)
    lis = jsonify(find_replicate(all_todos))

    return lis


@app.route('/delete', methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def senti():
    query_parameters = request.args
    ip_a = query_parameters.get('ip')
    # ip_a = str(ip_a)
    docs = db.collection('comments').where("ip", "==", ip_a).get()
    print(docs)
    for doc in docs:
        key = doc.id
        db.collection('comments').document(key).delete()
    return "done"


@app.route('/mail', methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def mail():
    mail_admin()
    return 1


@app.route('/analyze', methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def sentimental():
    query_parameters = request.args
    ip_a = query_parameters.get('ip')
    all_todos = [doc.to_dict() for doc in todo_ref.stream()]

    lis=jsonify(sentiment(all_todos,ip_a))
    print(lis)
    return lis




app.run(host='127.0.0.1', port=5010)

from flask import Flask, render_template, redirect, url_for, request
import os
import json
import re
import psycopg2 as dbapi2
from initdb import *
from user import User
from comment import Comment
from content import Content
from action import Action
from actor import Actor

app = Flask(__name__)


def get_elephantsql_dsn(vcap_services):
    """Returns the data source name for ElephantSQL."""
    parsed = json.loads(vcap_services)
    uri = parsed["elephantsql"][0]["credentials"]["uri"]
    match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
    user, password, host, _, port, dbname = match.groups()
    dsn = """user='{}' password='{}' host='{}' port={}
             dbname='{}'""".format(user, password, host, port, dbname)
    return dsn


@app.route('/clearuserdb')
def clear_userdb():
    drop_usertable(app.config['dsn'])
    return redirect(url_for('home'))

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        username = request.form['inputUsername']
        password = request.form['inputPassword']
        email = request.form['inputEmail']
        name = request.form['inputName']
        surname = request.form['inputSurname']
        user = User(username, password, email, name, surname, None, "dummyprofile.png")
        init_usertable(app.config['dsn'], user)
        return redirect(url_for('home'))

@app.route('/userdelete/<username>', methods=['GET', 'POST'])
def user_delete(username):
    if request.method == 'POST':
        deletefrom_usertable(app.config['dsn'], username)
        return redirect(url_for('users_list'))
    else:
        return render_template('confirmuserdelete.html', username=username)

    

@app.route('/userslist')
def users_list():
    fixdrop_usertable(app.config['dsn'])
    alldata = getall_usertable(app.config['dsn'])
    return render_template('userslist.html', users = alldata)

@app.route('/useredit/<username>', methods=['GET', 'POST'])
def user_edit(username):
    if request.method == 'GET':
        getuser = getuser_usertable(app.config['dsn'], username)
        return render_template('useredit.html', user=getuser, username=username)
    else:
        name = request.form['inputName']
        surname = request.form['inputSurname']
        email = request.form['inputEmail']
        password = request.form['inputPassword']
        if len(password) == 0:
            user = User(username, "1", email, name, surname, None, "dummyprofile.png")
            edituserwopass_usertable(app.config['dsn'], user)
        else:
            user = User(username, password, email, name, surname, None, "dummyprofile.png")
            edituserwpass_usertable(app.config['dsn'], user)

        return redirect(url_for('users_list'))



@app.route('/timeline',methods=['GET', 'POST'])
def timeline():
    if request.method == 'GET':
        #This function creates COMMENTS table and inserts an example data into the table.
        username='Example Username'
        comment = 'Example Comment'
        contentid=1
        cmm = Comment(comment,contentid,username)
        init_commentTable(app.config['dsn'], cmm)
        init_actionTable(app.config['dsn'])
        getall = getAllActions(app.config['dsn'])
        return render_template('timeline.html',actionList = getall)
    else:
        username = request.form['inputUsername']
        contentid = 1
        actiontype = "comment"
        actioncomment = request.form['inputCommentary']
        date = "someDate"
        action = Action(username,contentid,actiontype,actioncomment,date)
        insert_actionTable(app.config['dsn'], action)
        return redirect(url_for('timeline'))

@app.route('/clearactiontable')
def clearActionTable():
     dropActionTable(app.config['dsn'])
     return redirect(url_for('timeline'))

@app.route('/actionModify/<username>', methods=['GET','POST']) 
def actionModify(username):
    if request.method == 'GET':
        thisaction = getAction(app.config['dsn'],username)
        return render_template('actionModify.html',action = thisaction, username = username)
    else:
        comment = request.form['inputComment']
        edit_Action(app.config['dsn'],comment,username)
        return redirect(url_for('timeline'))

@app.route('/deleteAction/<username>', methods=['GET','POST'])
def deleteAction(username):
    if request.method == 'POST':
        deleteActionFromTable(app.config['dsn'],username)
        return redirect(url_for('timeline'))
    else:
        return render_template('confirmactiondelete.html',username=username)

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/content')
def content():
    cont=Content("Professional", "Dusan Kovacevic", "135 min", "10/26/2016", "Theater", "professional.jpg")
    init_contenttable(app.config['dsn'], cont)
    return render_template('content.html')
@app.route('/contentslist')
def contents_list():
    allcontents = getall_contenttable(app.config['dsn'])
    return render_template('contentslist.html', contents = allcontents)
@app.route('/contentdelete/<contentid>', methods=['GET', 'POST'])
def content_delete(contentid):
    if request.method == 'POST':
        deletefrom_contenttable(app.config['dsn'], contentid)
        return redirect(url_for('contents_list'))
    else:
        return render_template('confirmcontentdelete.html', contentid=contentid)
@app.route('/contentedit/<contentid>', methods=['GET', 'POST'])
def content_edit(contentid):
    if request.method == 'GET':
        getcontent = getcontent_contenttable(app.config['dsn'], contentid)
        return render_template('contentedit.html', content=getcontent, contentid=contentid)
    else:
        title = request.form['inputTitle']
        artist = request.form['inputArtist']
        duration = request.form['inputDuration']
        date = request.form['inputDate']
        contentpic = request.form['inputCp']
        genres = request.form['inputGenres']
        content = Content(title, artist, duration, date, contentpic, genres)
        edit_content(app.config['dsn'], contentid,content)

        return redirect(url_for('contents_list'))
@app.route('/admin',methods=['GET', 'POST'])
def admin():
    if request.method=='GET':
        return render_template('contentadmin.html')
    else:
        title = request.form['inputTitle']
        artist = request.form['inputArtist']
        duration = request.form['inputDuration']
        date = request.form['inputDate']
        contentpic = request.form['inputCp']
        genres = request.form['inputGenres']
        content = Content(title,artist,duration,date,contentpic,genres)
        init_contenttable(app.config['dsn'], content)
        return redirect(url_for('admin'))

@app.route('/search')
def search():
    return render_template('searchresult.html')

@app.route('/actor', methods=['GET', 'POST'])
def actor():
    if request.method == 'GET':
        return render_template('actor.html')
    elif request.method == 'POST':
        if request.form['submit'] == 'Add':
            actorname = request.form['ActorName']
            actorsurname = request.form['ActorSurname']
            actorbirthday = request.form['ActorBirthday']
            init_actortable(app.config['dsn'], actorname, actorsurname, actorbirthday)
            return render_template('actor.html')
        elif request.form['submit'] == 'Delete':
            actorID = request.form['ActorID']
            deleteactor(app.config['dsn'], actorID)
            return render_template('actor.html')
        elif request.form['submit'] == 'Edit':
            actorID = request.form['ActorID']
            actorname = request.form['ActorName']
            actorsurname = request.form['ActorSurname']
            actorbirthday = request.form['ActorBirthday']
            actortoedit = Actor(actorname, actorsurname, actorbirthday)
            editactor(app.config['dsn'], actorID, actortoedit)
            return render_template('actor.html')

@app.route('/actorlist')
def actor_list():
    alldata = getall_actortable(app.config['dsn'])
    return render_template('actorlist.html', actors = alldata)

if __name__ == '__main__':
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True

    VCAP_SERVICES = os.getenv('VCAP_SERVICES')
    if VCAP_SERVICES is not None:
        app.config['dsn'] = get_elephantsql_dsn(VCAP_SERVICES)
    else:
        app.config['dsn'] = """user='postgres' password='123456' host='localhost' port=5432 dbname='itucsdb1610'"""
    app.run(host='0.0.0.0', port=port, debug=debug)
    

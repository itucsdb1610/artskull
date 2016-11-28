from flask import Flask, render_template, redirect, url_for, request, session, escape, request
import os
import json
import re
import psycopg2 as dbapi2
import datetime
from initdb import *
from user import User
from comment import Comment
from content import Content
from action import Action
from actor import Actor
import time

app = Flask(__name__)
app.secret_key = 'MerhabaITUCSDB1610'

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
    if 'username' in session:
        return redirect(url_for('timeline'))

    if request.method == 'POST':
        username = request.form['inputUsername']
        password = request.form['inputPassword']
        email = request.form['inputEmail']
        name = request.form['inputName']
        surname = request.form['inputSurname']
        user = User(username, password, email, name, surname, "http://www.sbsc.in/images/dummy-profile-pic.png")
        init_usertable(app.config['dsn'], user)
        return redirect(url_for('user_login'))

    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def user_login():
    error = None
    if 'username' in session:
        return redirect(url_for('timeline'))

    if request.method == 'POST':
        username = request.form['inputUsername']
        password = request.form['inputPassword']
        if isuser_intable(app.config['dsn'], username, password):
            session['username'] = username
            return redirect(url_for('timeline'))
        else:
            error = "Invalid credentials"

    return render_template('login.html')

@app.route('/logout')
def user_logout():
    if 'username' not in session:
        return redirect(url_for('user_login'))
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/userdelete/<username>', methods=['GET', 'POST'])
def user_delete(username):
    if 'username' not in session:
        return redirect(url_for('user_login'))

    if request.method == 'POST':
        deletefrom_usertable(app.config['dsn'], username)
        return redirect(url_for('users_list'))
    else:
        return render_template('confirmuserdelete.html', username=username)

    

@app.route('/userslist')
def users_list():
    if 'username' not in session:
        return redirect(url_for('user_login'))

    fixdrop_usertable(app.config['dsn'])
    alldata = getall_usertable(app.config['dsn'])
    return render_template('userslist.html', users = alldata)

@app.route('/useredit/<username>', methods=['GET', 'POST'])
def user_edit(username):
    if 'username' not in session:
        return redirect(url_for('user_login'))

    if request.method == 'GET':
        getuser = getuser_usertable(app.config['dsn'], username)
        return render_template('useredit.html', user=getuser, username=username)
    else:
        name = request.form['inputName']
        surname = request.form['inputSurname']
        email = request.form['inputEmail']
        password = request.form['inputPassword']
        profpic = request.form['inputProfPic']
        if len(password) == 0:
            user = User(username, "1", email, name, surname, profpic)
            edituserwopass_usertable(app.config['dsn'], user)
        else:
            user = User(username, password, email, name, surname, profpic)
            edituserwpass_usertable(app.config['dsn'], user)

        return redirect(url_for('users_list'))

@app.route('/useredit/editgenre/<username>', methods=['GET', 'POST'])
def add_genre_user(username):
    if 'username' not in session:
        return redirect(url_for('user_login'))

    if request.method == 'POST':
        genre = request.form['inputGenres']
        order = request.form['inputImportance']
        init_genreTable(app.config['dsn'], username, genre, order)
        alldata = getall_genres(app.config['dsn'],username)
    else:
        alldata = getall_genres(app.config['dsn'],username)        

    return render_template('editgenre.html', genres=alldata, username=username)

@app.route('/useredit/editgenre/deletegenre/<username>', methods=['GET','POST'])
def genre_delete(username):
    if 'username' not in session:
        return redirect(url_for('user_login'))

    if request.method == 'GET':
        genre = request.args.get('genre')
        print(username)
        print(genre)
        delete_genreTable(app.config['dsn'], username, genre)

    return redirect(url_for('users_list'))


@app.route('/commentslist')
def comments_list():
    if 'username' not in session:
        return redirect(url_for('user_login'))

    fixdrop_usertable(app.config['dsn'])
    alldata = getall_commenttable(app.config['dsn'])
    return render_template('commentslist.html', comments = alldata)
	
@app.route('/commentedit/<commentid>', methods=['GET', 'POST'])
def comment_edit(commentid):
    if 'username' not in session:
        return redirect(url_for('user_login'))

    if request.method == 'GET':
        actualcomment = getcomment(app.config['dsn'], commentid)
        return render_template('commentedit.html', comment=getcomment, commentid=commentid)
    else:
        inusername = request.form['inusername']
        incomm = request.form['incomment']
        comment = Comment(incomm,1,inusername)
        edit_comment(app.config['dsn'], commentid, comment)
        return redirect(url_for('comments_list'))
		
@app.route('/commentdelete/<commentid>', methods=['GET', 'POST'])
def comment_delete(commentid):
    if 'username' not in session:
        return redirect(url_for('user_login'))

    if request.method == 'POST':
        deletefrom_commenttable(app.config['dsn'], commentid)
        return redirect(url_for('comments_list'))
    else:
        return render_template('confirmcommentdelete.html', commentid=commentid)

@app.route('/dropcomments')
def dropcomments():
    if 'username' not in session:
        return redirect(url_for('user_login'))

    drop_commenttable(app.config['dsn'])
    return redirect(url_for('comments_list'))	

@app.route('/timeline',methods=['GET', 'POST'])
def timeline():
    if 'username' not in session:
        return redirect(url_for('user_login'))

    if request.method == 'GET':
        init_commentTable(app.config['dsn'])
        init_actionTable(app.config['dsn'])
        getall = getAction(app.config['dsn'],session['username'])
        getallcomments = getall_commenttable(app.config['dsn'])
        return render_template('timeline.html',actionList = getall, commentList = getallcomments)
    else:
        username = session['username']
        actioncomment = request.form['inputCommentary']
        actionid = request.form['actionid']
        cmm = Comment(actioncomment,contentid, username)
        insert_commenttable(app.config['dsn'], cmm)
        return redirect(url_for('timeline'))

@app.route('/clearactiontable')
def clearActionTable():
    if 'username' not in session:
        return redirect(url_for('user_login'))

    dropActionTable(app.config['dsn'])
    return redirect(url_for('timeline'))

@app.route('/actionModify/<username>', methods=['GET','POST']) 
def actionModify(username):
    if 'username' not in session:
        return redirect(url_for('user_login'))

    if request.method == 'GET':
        thisaction = getAction(app.config['dsn'],username)
        return render_template('actionModify.html',action = thisaction, username = username)
    else:
        comment = request.form['inputComment']
        edit_Action(app.config['dsn'],comment,username)
        return redirect(url_for('timeline'))

@app.route('/deleteAction/<username>', methods=['GET','POST'])
def deleteAction(username):
    if 'username' not in session:
        return redirect(url_for('user_login'))

    if request.method == 'POST':
        deleteActionFromTable(app.config['dsn'],username)
        return redirect(url_for('timeline'))
    else:
        return render_template('confirmactiondelete.html',username=username)

@app.route('/profile/<username>')
def profile(username):
    if 'username' not in session:
        return redirect(url_for('user_login'))

    if session['username'] == username:
        same = True
    else:
        same = False

    getUsername = session['username']
    getUser = getuser_usertable(app.config['dsn'], username)
    getGenres = getall_genres(app.config['dsn'], username)
    getFollowingCounts = get_following_counts(app.config['dsn'], username)
    isFollowing = is_following(app.config['dsn'],getUsername, username)
    getFollowerCounts = get_followed_counts(app.config['dsn'],username)
    
    return render_template('profile.html', user=getUser, genres=getGenres, username=username, followingCounts=getFollowingCounts, followedCounts=getFollowerCounts, follows=isFollowing, same=same)

@app.route('/follow/<username>')
def follow(username):
    if 'username' not in session:
        return redirect(url_for('user_login'))

    if session['username'] == username:
        return redirect(url_for('timeline'))

    date = time.strftime("%d/%m/%Y")
    init_followUserUser(app.config['dsn'], session['username'], username, date)

    return redirect(url_for('timeline'))

@app.route('/unfollow/<username>')
def unfollow(username):
    if 'username' not in session:
        return redirect(url_for('user_login'))

    if session['username'] == username:
        return redirect(url_for('timeline'))

    unfollow_followUserUser(app.config['dsn'], session['username'], username)

    return redirect(url_for('timeline'))

@app.route('/following/<username>')
def following(username):
    if 'username' not in session:
        return redirect(url_for('user_login'))

    getFollowing = get_allfollowing(app.config['dsn'], username)

    return render_template('followlist.html', follow=getFollowing, username=username)

@app.route('/followed/<username>')
def followed(username):
    if 'username' not in session:
        return redirect(url_for('user_login'))

    getFollowed = get_allfollower(app.config['dsn'], username)

    return render_template('followlist.html', follow=getFollowed, username=username)
    
@app.route('/content')
def content():
    if 'username' not in session:
        return redirect(url_for('user_login'))

    return render_template('content.html')

@app.route('/content/<contentid>', methods=['GET', 'POST'])
def contentstatic(contentid):
    if 'username' not in session:
        return redirect(url_for('user_login'))

    if request.method == 'GET':
        getcontentAction = getcontent_action(app.config['dsn'], contentid) 
        getcontent = getcontent_contenttable(app.config['dsn'], contentid)
        return render_template('contentstatic.html',content = getcontent, contentid=contentid, contentaction=getcontentAction)

    elif request.method == 'POST':#this section belongs to Mahmut Lutfullah ÖZBİLEN
        if request.form['submit'] == 'Share':
            username = session['username']
            actiontype = "comment"
            actioncomment = request.form['inputCommentary']
            date = datetime.datetime.now()
            action = Action(username,contentid,actiontype,actioncomment,date)
            cmm = Comment(actioncomment,contentid, username)
            insert_actionTable(app.config['dsn'], action)
            return redirect(url_for('contentstatic',contentid=contentid))
    else:
        return render_template('content.html')



@app.route('/contentslist')
def contents_list():
    if 'username' not in session:
        return redirect(url_for('user_login'))

    allcontents = getall_contenttable(app.config['dsn'])
    return render_template('contentslist.html', contents = allcontents)

@app.route('/contentdelete/<contentid>', methods=['GET', 'POST'])
def content_delete(contentid):
    if 'username' not in session:
        return redirect(url_for('user_login'))

    if request.method == 'POST':
        deletefrom_contenttable(app.config['dsn'], contentid)
        return redirect(url_for('contents_list'))
    else:
        return render_template('confirmcontentdelete.html', contentid=contentid)

@app.route('/contentedit/<contentid>', methods=['GET', 'POST'])
def content_edit(contentid):
    if 'username' not in session:
        return redirect(url_for('user_login'))

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
    if 'username' not in session:
        return redirect(url_for('user_login'))

    if request.method=='GET':
        return render_template('contentadmin.html')
    else:
        title = request.form['inputTitle']
        artist = request.form['inputArtist']
        duration = request.form['inputDuration']
        date = request.form['inputDate']
        contentpic = request.form['inputCp']
        genres = request.form['inputGenres']
        content = Content(title,artist,duration,date,genres,contentpic)
        init_contenttable(app.config['dsn'], content)
        return redirect(url_for('admin'))

@app.route('/search', methods=['GET','POST'])
def search():
    if 'username' not in session:
        return redirect(url_for('user_login'))

    keyword = request.form['searchbox']

    searchAllUsers = search_user_table(app.config['dsn'], keyword)
    return render_template('searchresult.html', results=searchAllUsers, keyword=keyword)

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
        elif request.form['submit'] == 'Search':
            actortosearch = request.form['ActorName']
            actorarr = searchactor(app.config['dsn'], actortosearch)
            return render_template('actorlist.html', actors = actorarr)
            return render_template('actor.html')

@app.route('/actorlist')
def actor_list():
    alldata = getall_actortable(app.config['dsn'])
    return render_template('actorlist.html', actors = alldata)

@app.route('/actordelete/<actorid>', methods=['GET', 'POST'])
def actor_delete(actorid):
    if request.method == 'POST':
        deleteactor(app.config['dsn'], actorid)
        return redirect(url_for('actor'))
    else:
        return render_template('actordelete.html', actorid=actorid)

@app.route('/actoredit/<actorid>', methods=['GET', 'POST'])
def actor_edit(actorid):
    if request.method == 'GET':
        actortoedit = searchactor_byid(app.config['dsn'], actorid)
        return render_template('actoredit.html', editactor=actortoedit, actorid=actorid)
    else:
        actorname = request.form['ActorName']
        actorsurname = request.form['ActorSurname']
        actorbirthday = request.form['ActorBirthday']
        actortoedit = Actor(actorname, actorsurname, actorbirthday)
        editactor(app.config['dsn'], actorid, actortoedit)

        return redirect(url_for('actor'))

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
    

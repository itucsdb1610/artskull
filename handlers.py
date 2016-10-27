from flask import Blueprint, render_template
from flask import current_app, request, redirect, url_for

site = Blueprint('site', __name__)

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/timeline')
def timeline():
    return render_template('timeline.html')

@site.route('/profile')
def profile():
    return render_template('profile.html')

@site.route('/content')
def content():
    return render_template('content.html')

@site.route('/admin')
def admin():
    return render_template('contentadmin.html')

@site.route('/search')
def search():
    return render_template('searchresult.html')
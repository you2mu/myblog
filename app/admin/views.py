from flask import request, session, redirect,url_for, render_template
from . import admin
from .. import db
from ..models import Adm, Article


@admin.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        if request.form['name'] == 'admin' and request.form['password'] =='yl4321':
            session['name'] = request.form['name']
            return redirect(url_for('.choose'))
        else:
            return redirect(url_for('.login'))
    return render_template('login.html')

@admin.route('/choose')
def choose():
    if 'name' in session:
        return render_template('choose.html')
    return render_template('404.html'),404

@admin.route('/edit',methods=['GET','POST'])
def edit():
    '''
    网站的后台数据处理数据
    '''
    if 'name' in session:
        if request.method == 'POST':
            title = request.form['title']
            tag = request.form['tag']
            content = request.form['content']
            article = Article(tag=tag,title=title,content=content)
            db.session.add(article)
            return redirect(url_for('.edit'))
    else:
        return render_template('404.html'),404
    return render_template('admin.html')

@admin.route('/managedata',methods=['GET','POST'])
def managedata():
    if 'name' in session :
        return render_template('data.html')
    return render_template('404.html'),404

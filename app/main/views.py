from flask import render_template, request
from . import main
# from .. import db
from ..models import Article

@main.route('/')
def index():
    page = request.args.get('page',0,type=int)
    pagination = Article.query.order_by(Article.time.desc()).paginate(page, per_page=10,
     error_out=False)
    posts = pagination.items
    # posts = Article.query.order_by(Article.time.desc()).all()
    return render_template('test.html',posts=posts, pagination=pagination)

@main.route('/post/<int:id>')
def post(id):
    post = Article.query.get_or_404(id)
    return render_template('post.html',post=post)

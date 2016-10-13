from flask import render_template, jsonify, request,url_for
from . import api
from .. import db
from ..models import Article

@api.route('/posts/')
def get_posts():
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.order_by(Article.time.desc()).paginate(
        page, per_page=10,
        error_out=False)
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_posts', page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_posts', page=page+1, _external=True)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total,
    })

@api.route('/posts/<int:id>')
def get_post(id):
    post = Article.query.get_or_404(id)
    return jsonify(post.to_json() )

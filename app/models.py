from flask import url_for
from datetime import datetime
from markdown import markdown
import bleach
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

class Article(db.Model):
    __tablename__ = 'articles'
    id =db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(64), index=True)
    title = db.Column(db.String(64), unique=True,index=True)
    content = db.Column(db.Text)
    time = db.Column(db.String(64),index=True,default=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
    content_html = db.Column(db.Text)

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py

        seed()
        for i in range(count):
            p = Article(content=forgery_py.lorem_ipsum.sentences(randint(1, 5)),
                     time=forgery_py.date.date(True),title=i,tag='Python'
                     )
            db.session.add(p)
            db.session.commit()

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p', 'hr']
        target.content_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

    def to_json(self):
        json_post = {
        'url': url_for('api.get_post', id=self.id, _external=True),
        'tag': self.tag,
        'title':self.title,
        'content':self.content,
        'content_html':self.content_html,
        'time':self.time,
        'id':self.id
        }
        return json_post

db.event.listen(Article.content, 'set', Article.on_changed_body)


class Adm(db.Model):
    __tablename__ = 'adm'
    id = db.Column(db.Integer, primary_key=True)
    adm = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('no permission read password')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

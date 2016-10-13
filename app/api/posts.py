from flask import render_template
from . import api

@api.route('/test')
def test():
    return 'test api'

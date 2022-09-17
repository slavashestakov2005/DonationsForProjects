from backend import app
from flask import render_template
from flask_cors import cross_origin
from jinja2 import TemplateNotFound
from ..help import not_found_error
from ..database import ProjectsTable
'''
                    params()            Общие параметры.
    /               index()             Возвращает стартовую страницу.
    /<path>         static_file(path)   Возвращает страницу или файл.
'''


def params():
    return {'projects': ProjectsTable.select_all()}


@app.route('/')
@app.route('/index.html')
@cross_origin()
def index():
    return render_template('index.html', **params())


@app.route('/<path:path>')
@cross_origin()
def static_file(path):
    parts = [x.lower() for x in path.rsplit('.', 1)]
    try:
        if len(parts) >= 2 and parts[1] == 'html':
            return render_template(path, **params())
        return app.send_static_file(path)
    except TemplateNotFound:
        return not_found_error()

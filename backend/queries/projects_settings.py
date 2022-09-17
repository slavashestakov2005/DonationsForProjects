from backend import app
from flask import render_template, request
from flask_cors import cross_origin
from flask_login import login_required
from ..help import empty_checker, parse_checkbox, not_found_error
from ..database import ProjectsTable, Project
'''
                        TEMPLATE            Имя шаблона с настройкой проектов.
                        TEMPLATE1           Имя шаблона с описанием одного проекта.
                        params()            Постоянные параметры шаблонов.
    /projects           project()           Пересылает на страницу с настройкой проектов.
    /project            proj()              Пересылает на страницу с одним проектом.
                        _add_project()      Добавляет проект по данным формы.
    /add_project        add_project()       Добавляет проект от имени администратора.
    /propose_project    propose_project()   Предлагает проект без входа на сайт.
    /edit_project       edit_project()      Редактирует проект.    
    /delete_project     delete_project()    Удаляет проект.
'''


TEMPLATE, TEMPLATE1 = 'settings_projects.html', 'project.html'


def params():
    return {'projects': ProjectsTable.select_all()}


@app.route("/projects")
@cross_origin()
@login_required
def projects():
    return render_template(TEMPLATE, **params())


@app.route("/project")
@cross_origin()
def proj():
    try:
        pid = int(request.args.get('id'))
        project = ProjectsTable.select(pid)
        if project.__is_none__ or not project.is_public():
            raise ValueError
    except Exception:
        return not_found_error()
    return render_template(TEMPLATE1, project=project, **params())


def _add_project(template, info_filed, public=False):
    try:
        name = request.form['name']
        description = request.form['description']
        cost = int(request.form['cost'])
        received = request.form['received']
        received = 0 if received == '' else int(received)
        author = request.form['author']
        author_contacts = request.form['author_contacts']
        executor = request.form['executor']
        executor_contacts = request.form['executor_contacts']
        other_info = request.form['other_info']
        empty_checker(name, description)
    except Exception:
        return render_template(template, **{info_filed: 'Поля заполнены не правильно'}, **params())

    project = Project([None, name, description, '', cost, received, author, author_contacts, executor,
                       executor_contacts, other_info, ''])
    project.set_public(public)
    ProjectsTable.insert(project)
    project = ProjectsTable.select_last()
    project.photo = parse_checkbox(project.id, 'logo.png', folder='Projects/')
    ProjectsTable.update(project)
    return render_template(template, **{info_filed: 'Проект добавлен'}, **params())


@app.route("/add_project", methods=['POST'])
@cross_origin()
@login_required
def add_project():
    public = request.form.get('public') or False
    return _add_project(TEMPLATE, 'error_add_project', public=public)


@app.route("/propose_project", methods=['POST'])
@cross_origin()
def propose_project():
    return _add_project('index.html', 'error_propose_project')


@app.route("/edit_project", methods=['POST'])
@cross_origin()
@login_required
def edit_project():
    try:
        id = int(request.form['id'])
        name = request.form['name']
        description = request.form['description']
        cost = request.form['cost']
        cost = None if cost == '' else int(cost)
        received = request.form['received']
        received = None if received == '' else int(received)
        author = request.form['author']
        author_contacts = request.form['author_contacts']
        executor = request.form['executor']
        executor_contacts = request.form['executor_contacts']
        other_info = request.form['other_info']
        public = request.form.get('public') or False
    except Exception:
        return render_template(TEMPLATE, error_edit_project='Поля заполнены не правильно', **params())

    project = ProjectsTable.select(id)
    if project.__is_none__:
        return render_template(TEMPLATE, error_edit_project='Не верный ID проекта', **params())
    if name:
        project.name = name
    if description:
        project.description = description
    if cost is not None:
        project.cost = cost
    if received is not None:
        project.received = received
    if author:
        project.author = author
    if author_contacts:
        project.author_contacts = author_contacts
    if executor:
        project.executor = executor
    if executor_contacts:
        project.executor_contacts = executor_contacts
    if other_info:
        project.other_info = other_info
    project.set_public(public)
    project.photo = parse_checkbox(project.id, project.photo, folder='Projects/')
    ProjectsTable.update(project)
    return render_template(TEMPLATE, error_edit_project='Проект изменён', **params())


@app.route("/delete_project", methods=['POST'])
@cross_origin()
@login_required
def delete_project():
    try:
        id = int(request.form['id'])
    except Exception:
        return render_template(TEMPLATE, error_delete_project='Поля заполнены не правильно', **params())

    project = ProjectsTable.select(id)
    if project.__is_none__:
        return render_template(TEMPLATE, error_delete_project='Не верный ID проекта', **params())
    ProjectsTable.delete(project)
    return render_template(TEMPLATE, error_delete_project='Проект удалён', **params())

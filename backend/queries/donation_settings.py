from backend import app
from flask import render_template, request
from flask_cors import cross_origin
from flask_login import login_required
from ..help import unix_time, not_found_error, TinkoffCard
from ..database import Donation, DonationsTable, ProjectsTable
from ..config import Config
'''
                                get_status()            Превращает Tinkoff-статус платежа в статус пожертвования.
                                TEMPLATE                Имя шаблона с регистрацией пожертвования.
                                TEMPLATE_ALL            Имя шаблона со списком пожертвований.
    /donate?id=<>               donate()                Регистрация пожертвования.
    /show_donations?id=<>       show_donations()        Показывает все пожертвования на проект.
    /update_donations?id=<>     update_donations()      Обновляет статусы пожертвований.
'''


def get_status(status):
    if status in Config.PAID_STATES:
        return Donation.PAID
    elif status in Config.NOT_PAID_STATES:
        return Donation.NOT_PAID
    return None


TEMPLATE, TEMPLATE_ALL = 'project.html', 'donations.html'


@app.route("/donate", methods=['POST'])
@cross_origin()
def donate():
    try:
        pid = int(request.form['id'])
        project = ProjectsTable.select(pid)
        name = request.form['name']
        amount = int(request.form['amount'])
        other_info = request.form['other_info']
        if project.__is_none__:
            return not_found_error()
        if amount <= 0:
            raise ValueError
    except Exception:
        return render_template(TEMPLATE, error_donate='Поля заполнены не правильно')

    donation = Donation([None, pid, name, amount, other_info, Donation.REQUEST_SUBMITTED, -1, unix_time()])
    DonationsTable.insert(donation)
    donation = DonationsTable.select_last()
    desc = 'Проект: {} Жертвователь: {}'.format(project.name, donation.name)
    error, url, payment = TinkoffCard.receipt(donation.amount, donation.id, desc)
    if error != '0':
        donation.status = Donation.ERROR
        DonationsTable.update(donation)
        return render_template(TEMPLATE, project=project, error_donate='Ошибка :(')
    donation.payment = payment
    DonationsTable.update(donation)
    return render_template(TEMPLATE, error_donate='Пожертвование зарегистрировано', project=project, url=url)


@app.route("/show_donations")
@cross_origin()
@login_required
def show_donations():
    try:
        pid = int(request.args.get('id'))
        project = ProjectsTable.select(pid)
        if project.__is_none__:
            raise ValueError
    except Exception:
        return not_found_error()

    donations = DonationsTable.select_by_project(pid)
    return render_template(TEMPLATE_ALL, donations=donations, project=project)


@app.route("/update_donations")
@cross_origin()
@login_required
def update_donations():
    try:
        pid = int(request.args.get('id'))
        project = ProjectsTable.select(pid)
        if project.__is_none__:
            raise ValueError
    except Exception:
        return not_found_error()

    donations = DonationsTable.select_by_project(pid)
    updated = False
    for donation in donations:
        error, status = TinkoffCard.get_state(donation.payment)
        status = get_status(status)
        if status and status != donation.status:
            donation.status = status
            DonationsTable.update(donation)
            if donation.status == Donation.PAID:
                project.received += donation.amount
                updated = True
    if updated:
        ProjectsTable.update(project)
    return render_template(TEMPLATE_ALL, donations=donations, project=project)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bottle import route, run, template, request, redirect, response
import bottle
import templates
import config
import datetime


def is_logined():
    return request.get_cookie("logined", secret='some-secret-key')


def check_login(f):
    def decorated(*args, **kwargs):
        if is_logined():
            return f(*args, **kwargs)
        else:
            redirect("/login")
    return decorated


def read_messages():
    def _stripped(e):
        return e.readline().rstrip()
    all_entries = []
    with open("database.txt") as d:
        while(True):
            entry = {}
            date = _stripped(d)
            if date == '':
                break
            entry['date'] = date
            entry['date_fmt'] = "{0}/{1}/{2} {3}:{4}".format(date[0:4], date[4:6], date[6:8], date[8:10], date[10:12])
            entry['title'] = _stripped(d)
            entry['categories'] = _stripped(d).split(',')
            entry['text'] = ''
            while(True):
                text = d.readline()
                if text.rstrip() == config.separator or text == '':
                    all_entries.append(entry)
                    break
                entry['text'] += text.rstrip()
    return all_entries


def write_record(file, date, title, category, text):
    def _writeln(file, line):
        file.write(line +  '\n')
    _writeln(file, date)
    _writeln(file, title)
    _writeln(file, ",".join(category))
    _writeln(file, text)
    _writeln(file, config.separator)


def new_entry(title, text, category):
    date = datetime.datetime.today()
    date_fmt = date.strftime("%Y%m%d%H%M%S")
    with open("database.txt", "a") as d:
        write_record(d, date_fmt, title, category, text)
    return


def edit_entry(date, title, text, category):
    messages = read_messages()
    with open("database.txt", "w") as d:
        for message in messages:
            if message['date'] == date:
                write_record(d, date, title, category, text)
            else:
                write_record(d, message['date'], message['title'], message['categories'], message['text'])
    return


def delete_entry(date):
    messages = read_messages()
    with open("database.txt", "w") as d:
        for message in messages:
            if message['date'] != date:
                write_record(d, message['date'], message['title'], message['categories'], message['text'])
    return


def find_entry(entry_id):
    messages = [m for m in read_messages() if m['date'] == entry_id]
    if messages:
        return messages[0]
    else:
        return None


def find_by_category(cat_id):
    messages = [m for m in read_messages() if cat_id in m['categories']]
    return messages


@route('/')
def index():
    return template(templates.main_page, logined = is_logined(), categories=config.categories, messages=reversed(read_messages()))


@route('/nb')
def notebook():
    with open("notebook.txt") as n:
        message = n.read()
    return template(templates.notebook_page, message=message)


@route('/nb', method='POST')
def save_notebook():
    message = request.forms.get('message')
    with open("notebook.txt", "w") as n:
        n.write(message)
    return template(templates.notebook_page, message=message)


def filter_text(text):
    return text.replace('\r\n', '<br>')

@route('/save', method='POST')
@check_login
def save():
    def update(text, start_marker, end_marker, formatstring):
        while(True):
            start = text.find(start_marker)
            end = text.find(end_marker)
            if start >=0 and end > start:
                text = formatstring.format(text[0:start], text[start+2:end], text[end+2:])
            else:
                break
        return text

    def update_link(text):
        return update(text, '[[', ']]', '{0} <a href={1} target="_blank">{1}</a> {2}')

    def update_images(text):
        return update(text, '{{', '}}', '{0} <img src={1}>{2}')

    date = request.forms.get('date')
    title = request.forms.get('title')
    message = update_images(update_link(request.forms.get('text').replace('\r\n', '<br>')))
    category = request.forms.getlist('category')
    if date:
        edit_entry(date, title, message, category)
    else:
        new_entry( title, message, category)
    redirect("/#" + date)


@route('/add')
def add ():
    if is_logined():
        categories = [(c, False) for c in config.categories]
        return template(templates.edit_page, title="", categories=categories, text="", date="")
    else:
        return template(templates.login_page,referer="/add")

@route('/delete/<entry_id>')
@check_login
def delete_request (entry_id):
    return template(templates.delete_page, date=entry_id)


@route('/delete', method='POST')
@check_login
def delete():
    delete_entry(request.forms.get('date'))
    redirect("/")


@route('/edit/<entry_id>')
def edit (entry_id):
    if is_logined():
        entry = find_entry(entry_id)
        if entry:
            categories = [(c, c in entry['categories']) for c in config.categories]
            return template(templates.edit_page,title=entry["title"],categories=categories, text=entry["text"].replace('<br>', '\n'), date=entry["date"])
        else:
            redirect("/")
    else:
        return template(templates.login_page,referer="/edit/{0}".format(entry_id))


@route('/cat/<cat_id>')
@check_login
def category (cat_id):
    return template(templates.categories_page, category = cat_id, messages=reversed(find_by_category(cat_id)))


@route('/login')
def login():
    return template(templates.login_page,referer=request.headers.get('Referer'))

@route('/exit')
def exit():
    response.set_cookie("logined", False, secret='some-secret-key')
    redirect("/")


@route('/login', method='POST')
def do_login():
    password = request.forms.get('password')
    if validate(password):
        response.set_cookie("logined", True, secret='some-secret-key')
        referer = request.forms.get('referer')
        redirect(referer)
    else:
        return templates.not_autorized_page


def validate(password):
    return password == config.password

#run(server='cgi')
if __name__ == "__main__":
    bottle.debug(True)
    run(reloader=True, port=8081)

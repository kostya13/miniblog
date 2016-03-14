#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from bottle import route, run, template, request, redirect, response
import bottle
import templates
import config
import datetime


def is_logined():
    return request.get_cookie("logined", secret='some-secret-key')


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
            entry['text'] = _stripped(d)
            if _stripped(d)  == config.separator:
                all_entries.append(entry)
            else:
                raise Exception()
    return all_entries


def write_record(file, date, title, category, text):
    def _writeln(file, line):
        file.write(line +  '\n')
    _writeln(file, date)
    _writeln(file, title)
    _writeln(file, ",".join(category))
    _writeln(file, text)
    _writeln(file, config.separator)


def edit_message(date, title, text, category):
    messages = read_messages()
    with open("database.txt", "w") as d:
        for message in messages:
            if message['date'] == date:
                write_record(d, date, title, category, text)
            else:
                write_record(d, message['date'], message['title'], message['categories'], message['text'])
    return


def new_message(title, text, category):
    date = datetime.datetime.today()
    date_fmt = date.strftime("%Y%m%d%H%M%S")
    with open("database.txt", "a") as d:
        write_record(d, date_fmt, title, category, text)
    return


@route('/')
def index():
    return template(templates.main_form, logined = is_logined(), categories=config.categories, messages=reversed(read_messages()))


@route('/nb')
def notebook():
    with open("notebook.txt") as n:
        message = n.read()
    return template(templates.notebook, message=message) 


@route('/nb', method='POST')
def save_notebook():
    message = request.forms.get('message')    
    with open("notebook.txt", "w") as n:
        n.write(message)
    return template(templates.notebook, message=message) 


@route('/save', method='POST')
def save():
    date = request.forms.get('date')
    title = request.forms.get('title')
    message = request.forms.get('text')
    category = request.forms.getlist('category')
    if date:
        edit_message(date, title, message, category)
    else:
        new_message( title, message, category)
    redirect("/")


@route('/add')
def add ():
    if is_logined():
        categories = [(c, False) for c in config.categories]
        return template(templates.edit_entry, title="", categories=categories, text="", date="")
    else:
        return template(templates.login_form,referer="/add")


@route('/edit/<entry_id>')
def edit (entry_id):
    if is_logined():
        messages =[m for m in read_messages() if m['date'] == entry_id]
        if messages: 
            message = messages[0]
            categories = [(c, c in m['categories']) for c in config.categories]
            return template(templates.edit_entry,title=message["title"],categories=categories, text=message["text"], date=message["date"])
        else:
            redirect("/")
    else:
        return template(templates.login_form,referer="/edit/{0}".format(entry_id))


@route('/login')
def login():
    return template(templates.login_form,referer=request.headers.get('Referer'))


@route('/login', method='POST')
def do_login():
    password = request.forms.get('password')
    if check_login(password):
        response.set_cookie("logined", True, secret='some-secret-key')
        referer = request.forms.get('referer')
        redirect(referer)
    else:
        return templates.not_autorized


def check_login(password):
    return True


if __name__ == "__main__":
    #run(server='cgi')
    bottle.debug(True)
    run(reloader=True, port=8081)

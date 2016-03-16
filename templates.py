# -*- coding: UTF-8 -*-

main_form = '''
<h1 style="font-size:30pt">Я оставлю это здесь...</h1>
<a href="/nb">Записная книжка</a>
<span style="margin-left:20px">
%if logined:
<a href="/add">Добавить запись</a>
%end
%if not logined:
    <span style="margin-left:50px">
    <a href="/login">Логин</a>
%end
%if logined:
<span style="margin-left:50px">
<a href="/exit">Выход</a>
%end
<div style="margin-top:5px">
<br>
  % for cat in categories:
  <a href='/cat/{{cat}}'>{{cat}}</a>&nbsp;&nbsp;&nbsp;
  %end
% for mes in messages:
<table style="font-size:150%" width=800>
  <tr><td><hr></td></tr>
  <tr><td><h3 style="margin-bottom:5px;" id="{{mes["date"]}}">{{mes["title"]}}</h3></td></tr>
  <tr><td>Дата: {{mes["date_fmt"]}}
  %if logined:
  <a style="margin-left:40px;" href='/edit/{{mes["date"]}}'>Редактировать</a><span ><a style="margin-left:100px;font-size:small" href='/delete/{{mes["date"]}}'>[X]</a>
  %end
  </td></tr>
  <tr><td>
  % for cat in mes["categories"]:
  <a href='/cat/{{cat}}'>{{cat}}</a>&nbsp;&nbsp;&nbsp;
  %end
  <div style="margin-top:20px">
  </td></tr>
  <tr><td>{{!mes["text"]}}</td></tr>
</table>
%end
'''

categories = '''
<h2>Категория: {{category}}</h2>
<a href="/">Главная</a><br><br>
% for mes in messages:
<table style="font-size:150%" width=800>
  <tr><td><hr></td></tr>
  <tr><td><h3 style="margin-bottom:5px;" id="{{mes["date"]}}">{{mes["title"]}}</h3></td></tr>
  <tr><td>Дата: {{mes["date_fmt"]}}
  <a style="margin-left:50px;" href='/edit/{{mes["date"]}}'>Редактировать</a><span ><a style="margin-left:100px;font-size:small" href='/delete/{{mes["date"]}}'>Удалить</a></td></tr>
  <tr><td>
  % for cat in mes["categories"]:
  <a href='/cat/{{cat}}'>{{cat}}</a>&nbsp;&nbsp;&nbsp;
  %end
  <div style="margin-top:20px">
  </td></tr>
  <tr><td>{{!mes["text"]}}</td></tr>
</table>
%end
'''

not_autorized = '''Пройдите авторизацию снова <a href="/login">login</a><br><br>
        <a href="/">Главная</a>
'''

edit_entry = '''
        <a href="/">Главная</a><br><br>
        <form action="/save" method="post">
            <input type="text" name="title" value="{{title}}" size="50">   
            <input name="date" value="{{date}}" type="hidden" />
            <br>
            %for cat in categories:
             <input type="checkbox" name="category" value="{{cat[0]}}"
             %if cat[1]: 
                checked
             %end
            >{{cat[0]}}
            %end
            <Br>
            <textarea name="text" cols="100" rows="30">{{text}}</textarea>
            <br>
            &#91;&#91;ссылка&#93;&#93;, &#123;&#123;ссылка на картинку&#125;&#125;
            <br>
            <input value="Сохранить" type="submit" />
        </form>
'''

delete_entry = '''
        <a href="/">Главная</a><br><br>
        <form action="/delete" method="post">
          Подтверждение удаления сообщения {{date}}<br>
          <input name="date" value="{{date}}" type="hidden" />
          <input value="Удалить" type="submit" />
         </form>
    '''

login_form = '''
        <form action="/login" method="post">
            Password: <input name="password" type="password" />
            <input name="referer" value="{{referer}}" type="hidden" />
            <input value="Логин" type="submit" />
        </form>
    '''
notebook = '''
        <a href="/">Главная</a><br><br>
        <form action="/nb" method="post">
          <input value="Сохранить" type="submit" />
          <br>
          <textarea name="message" cols="100" rows="30">{{message}}</textarea>
         </form>
    '''



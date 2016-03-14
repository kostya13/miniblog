# -*- coding: UTF-8 -*-

main_form = '''
<h1>Я оставлю это здесь</h2>
<a href="/nb">Записная книжка</a>
<span style="margin-left:20px">
<a href="/add">Добавить запись</a>
%if not logined:
    <a href="/login">login</a>
%end
<hr>
<br>
  % for cat in categories:
  <a href='/cat/{{cat}}'>{{cat}}</a>&nbsp;&nbsp;&nbsp;
  %end
<hr>
% for mes in messages:
<table>
  <tr><td style="font-weight: bold">{{mes["title"]}}</td></tr>
  <tr><td>Дата: {{mes["date_fmt"]}}
  <a style="margin-left:50px;" href='/edit/{{mes["date"]}}'>Редактировать</a><span ><a style="margin-left:100px;font-size:small" href='/del/{{mes["date"]}}'>Удалить</a></td></tr>

  <tr><td>
  % for cat in mes["categories"]:
  <a href='/cat/{{cat}}'>{{cat}}</a>
  %end
  </td></tr>
  <tr><td>{{mes["text"]}}</td></tr>
</table>
<hr>
%end
'''

not_autorized = '''Пройдите авторизацию <a href="/login">login</a>'''

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
            <input value="Сохранить" type="submit" />
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

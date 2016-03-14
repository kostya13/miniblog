# -*- coding: UTF-8 -*-
main_form = '''
<h1>Я оставлю это здесь</h2>
<a href="/nb">notebook</a>
<a href="/add">add</a>
%if not logined:
    <a href="/login">login</a>
%end
<br>
<hr>
% for mes in messages:
<table>
  <tr><td>{{mes["title"]}}</td></tr>
  <tr><td><a href='/edit/{{mes["date"]}}'>edit</a></td></tr>
  <tr><td>{{mes["date"]}}</td></tr>
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

not_autorized = '''Please login  <a href="/login">login</a>'''

edit_entry = '''
        <a href="/">Main</a>
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
            <input value="Save" type="submit" />
        </form>
'''

login_form = '''
        <form action="/login" method="post">
            Password: <input name="password" type="password" />
            <input name="referer" value="{{referer}}" type="hidden" />
            <input value="Login" type="submit" />
        </form>
    '''
notebook = '''
        <a href="/">Main</a>
        <form action="/nb" method="post">
            <textarea name="message" cols="100" rows="30">{{message}}</textarea>
            <br>
            <input value="Save" type="submit" />
        </form>
    '''


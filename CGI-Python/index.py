# -*- coding: utf-8 -*-
import os


def greet(name):
    print('<h1>Привет, ' + name + '!</h1>')
    print('<h3>И хорошего дня!</h3>')


print('HTTP/1.0 200 OK')
print('Content-Type: text/html; charset=utf-8\n')

print('<!DOCTYPE html>')
print('<html>')
print('<head>')
print('<title>Hello</title>')
print('<meta charset="utf-8">')
print('</head>')
print('<body>')

if 'QUERY_STRING' in os.environ and os.environ['QUERY_STRING']:
    for p in os.environ['QUERY_STRING'].split("&"):
        if p[0:5] == "name=":
            greet(p[5:])
if 'HTTP_NAME' in os.environ:
    greet(os.environ['HTTP_NAME'])

print('</body>')
print('</html>')
# coding=UTF-8

import cherrypy
import codecs
import mysql.connector
import settings
import os, os.path
import types
import json
import zlib
import base64

from Cheetah.Template import Template
from datetime import date
from datetime import datetime, timedelta
from copy import copy
from functools import partial


server_host = settings.server_host
server_port = settings.server_port


def error_page(message="Ошибка сервера. Обратитесь к администратору."):
    return message


class Root(object):
    @cherrypy.expose
    def index(self):
        try:
            main_page = os.path.join('html', 'nonogram.html')
            f = codecs.open(main_page, encoding='utf-8')
            temp = f.read()
            rend = Template(temp)
            return str(rend)
        except Exception as e:
            cherrypy.log("Index page. Template Render Failure!", traceback=True)
            return error_page(str(e))

    @cherrypy.expose
    def create(self, width, height, name, nonogram):
        try:
            cnx = mysql.connector.connect(user=settings.user,
                                          password=settings.password,
                                          host=settings.host,
                                          database=settings.database)
            cnx.autocommit = True
            cursor = cnx.cursor()
            query = "INSERT INTO nonograms (json, name, width, height) VALUES (%s, %s, %s, %s)"
            encoded_nonogram = base64.b64encode(zlib.compress(nonogram.encode()))
            cursor.execute(query, [encoded_nonogram, name, width, height])
            return str(cursor.lastrowid)
        except Exception as e:
            cherrypy.log("Create handler. Failure!", traceback=True)
            return error_page(str(e))

    @cherrypy.expose
    def get_list(self):
        try:
            cnx = mysql.connector.connect(user=settings.user,
                                          password=settings.password,
                                          host=settings.host,
                                          database=settings.database)
            cnx.autocommit = True
            cursor = cnx.cursor()
            query = "SELECT id, name FROM nonograms"
            cursor.execute(query, [])
            
            ret_string = \
                "<div class=\"has-text-centered has-text-black is-size-5\">"\
                    "Try to solve this:"\
                "</div>"\
                "<div class=\"buttons\">"
            rows = cursor.fetchall()
            for nonogram in rows:
                id = str(nonogram[0])
                name = str(nonogram[1])
                ret_string += \
                    "<a class=\"button is-info is-fullwidth\""\
                        "onclick='get_nonogram(" + id + ")' id='" + id + "'>" + name \
                    + "</a>"
            ret_string += "</div>"

            return ret_string
        except Exception as e:
            cherrypy.log("Create handler. Failure!", traceback=True)
            return error_page(str(e))

    @cherrypy.expose
    def get_nonogram(self, id):
        try:
            cnx = mysql.connector.connect(user=settings.user,
                                          password=settings.password,
                                          host=settings.host,
                                          database=settings.database)
            cnx.autocommit = True
            cursor = cnx.cursor()
            query = "SELECT json FROM nonograms WHERE id = %s"
            cursor.execute(query, [id])

            rows = cursor.fetchall()

            return zlib.decompress(base64.b64decode(rows[0][0]))
        except Exception as e:
            cherrypy.log("Get nonogramm. Failure!", traceback=True)
            return error_page(str(e))

if __name__ == '__main__':
    cherrypy.config.update({'server.socket_host': server_host, 'server.socket_port': server_port,})
    cherrypy.quickstart(Root(), '/', "app.conf")

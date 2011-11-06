# Applicaton: jsontest1
#
# Using json and sqlalchemy and web py to serve county info for states of Missouri and Kansas
# Also uses mod_wsgi


import os
import web
import json
import sys

from web.contrib.template import render_mako

sys.path.append(os.path.dirname(__file__))

from countiesinstate import *

urls = (
    '/', 'jsontest3',
    '/countiesinstate/(.*)', 'countiesinstate'
)

#### Templates
#render = web.template.render('templates', base='base')

# input_encoding and output_encoding is important for unicode
# template file. Reference:
# http://www.makotemplates.org/docs/documentation.html#unicode
render = render_mako(
        directories=['templates'],
        input_encoding='utf-8',
        output_encoding='utf-8',
        )


app = web.application(urls, globals())
curdir = os.path.dirname(__file__)
session = web.session.Session(app, web.session.DiskStore(os.path.join(curdir,'sessions')),)
application = app.wsgifunc()


class jsontest3:
    def __init__(self):
        # set current directory to path of this script so templates can be found
        base_dir = os.path.dirname(os.path.realpath(__file__))
        os.chdir(base_dir)
        return

    def GET(self):
        """ Show page """
        #return render.default()
        return render.defaultmako(name='stuff')


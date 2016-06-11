#!usr/bin/env python
# -*- coding: utf-8 -*-
import os
# import sys

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.assets import Environment, Bundle
from codingpy import *

try:
    import local_config
except:
    pass

app = create_app(os.environ.get('APP_CONFIG') or 'default')

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


bundles = {

    'home_js': Bundle(
        'js/jquery-2.1.4.min.js',
        'js/modernizr.js',
        'vendor/semantic-ui/semantic.min.js',
        'vendor/glide/glide.min.js',
        'js/lazyloadxt.js',
        'js/lazyloadxt.bg.js',
        'js/jquery.infinitescroll.min.js',
        output='gen/home.js'),

    'home_css': Bundle(
        'vendor/normalize.min.css',
        'vendor/semantic-ui/semantic.css',
        'vendor/glide/css/glide.core.min.css',
        'vendor/glide/css/glide.theme.min.css',
        'style.css',
        'codehilite.css',
        depends='style.css',
        output='gen/home.css'),

}

assets = Environment(app)

assets.register(bundles)


@manager.shell
def make_shell_context():
    return dict(
        app=app, db=db, User=User, Role=Role, Permission=Permission,
        Category=Category, Tag=Tag, Article=Article, Topic=Topic,
        Label=Label
    )


@manager.command
def test(coverage=False):
    """Run unit tests and/or covrage reports
    """
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    manager.run()

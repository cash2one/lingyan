# coding: utf-8
from fabric.api import run, env, cd, prefix, shell_env, local
from local_config import HOST_STRING


def deploy():
    env.host_string = HOST_STRING
    with cd('/home/flask/source/codingpy'):
        with shell_env(MODE='PRODUCTION'):
            run('git reset --hard HEAD')
            run('git pull')
            with prefix('source /home/flask/flaskenv/bin/activate'):
                run('pip install -r requirements.txt')
                run('python manage.py db upgrade')
                run('python manage.py build')
            run('supervisorctl restart codingpy')


def restart():
    env.host_string = HOST_STRING
    with cd('/home/flask/source/codingpy'):
        with shell_env(MODE='PRODUCTION'):
            run('git reset --hard HEAD')
            run('git pull')
        run('supervisorctl restart codingpy')

def stop():
    env.host_string = HOST_STRING
    with cd('/home/flask/source/codingpy'):
        run('service nginx stop')
        run('supervisorctl stop codingpy')
        
def pull():
    env.host_string = HOST_STRING
    with cd('/home/flask/source/codingpy'):
        with shell_env(MODE='PRODUCTION'):
            run('git reset --hard HEAD')
            run('git pull')

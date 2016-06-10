from __future__ import unicode_literals
import multiprocessing

bind = "unix:/home/flask/source/codingpy/gunicorn.sock"
workers = multiprocessing.cpu_count() * 2 + 1
errorlog = "/home/flask/source/codingpy/codingpy_error.log"
loglevel = "error"
proc_name = "codingpy"

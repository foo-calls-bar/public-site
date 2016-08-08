user               = None
group              = None
bind               = 'unix:/var/tmp/gunicorn.sock'
pidfile            = '/var/tmp/gunicorn.pid'
errorlog           = '/home/django/logs/gunicorn_error.log'
accesslog          = '/home/django/logs/gunicorn_access.log'
working_dir        = '/home/django/agcs'
chdir              = working_dir
loglevel           = 'info'
backlog            = 2048
worker_connections = 1000
timeout            = 30
keepalive          = 2
umask              = 0
debug              = False
spew               = False
daemon             = False
proc_name          = None
tmp_upload_dir     = None


try:
    from agcs_utils.utils import num_cpus
    workers = 2 * num_cpus() + 1
    del(num_cpus)
except:
    workers = 3

try:
    import sys
    sys.path.index(working_dir)
except ValueError:
    sys.path.insert(0, working_dir)
finally:
    del(sys)

try:
    from importlib import import_module
    from os import getenv
    debug = import_module(getenv('DJANGO_SETTINGS_MODULE')).DEBUG
except AttributeError:
    debug = debug
finally:
    del(getenv, import_module)

loglevel = debug and 'debug' or 'info'

def post_fork(server, worker):
    pass
    #server.log.info("Worker spawned (pid: %s)", worker.pid)

def pre_fork(server, worker):
    pass
def pre_exec(server):
    server.log.info("Forked child, re-executing.")
def when_ready(server):
    server.log.info("Server is ready. Spawning workers")
def worker_abort(worker):
    worker.log.info("worker received SIGABRT signal")
def worker_int(worker):
    worker.log.info("worker received INT or QUIT signal")
    import threading, sys, traceback
    id2name = dict([(th.ident, th.name) for th in threading.enumerate()])
    code = []
    for threadId, stack in sys._current_frames().items():
        code.append("\n# Thread: %s(%d)" % (id2name.get(threadId,""),
            threadId))
        for filename, lineno, name, line in traceback.extract_stack(stack):
            code.append('File: "%s", line %d, in %s' % (filename,
                lineno, name))
            if line:
                code.append("  %s" % (line.strip()))
    worker.log.debug("\n".join(code))

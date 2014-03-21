
from watchdog.tricks import Trick
from timeit import default_timer as timer
from signal import signal, SIGTERM
from utile import get_pid_list, process_name, swap_save, enforce
from threading import Thread
from subprocess import check_output
from Queue import Queue
from urllib import urlopen
import logging.config
import os
import errno
import time
import sys

DEFAULT_LOGGING = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)5s - %(message)s',
        },
    },
    'handlers': {
        'default': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'INFO',
        },
    }
}


class BaseReloader(Trick):
    def __init__(
            self, log_config=None, source_directory=None, ignore_period=1,
            reload_delay=0.1, **kwargs):
        super(BaseReloader, self).__init__(**kwargs)
        self.source_directory = source_directory
        self.ignore_period = ignore_period
        self.reload_delay = reload_delay
        self.last_reload = 0
        log_config = log_config or DEFAULT_LOGGING
        logging.config.dictConfig(log_config)
        logging.info('Reloader started PID[%s]' % os.getpid())
        signal(SIGTERM, self.exit)

    def exit(self, signum, frame):
        logging.info('Reloader exiting PID[%s]' % os.getpid())
        sys.exit()

    def on_any_event(self, event):
        if timer() - self.last_reload < self.ignore_period:
            logging.info('ignored event %r' % event)
        else:
            logging.info('reload event %r' % event)
            if self.reload_delay:
                msg = 'sleeping for reload delay of %ss' % self.reload_delay
                logging.info(msg)
                time.sleep(self.reload_delay)
            try:
                self.reload()
            except:
                logging.exception('exception occurred in reload()')
            self.last_reload = timer()


class CommandReloader(BaseReloader):
    def __init__(self, command, **kwargs):
        super(CommandReloader, self).__init__(**kwargs)
        self.command = command

    def reload(self):
        check_output(self.command)


def fetch_worker(url, statsq):
    try:
        start = timer()
        urlopen(url).read()
        statsq.put((timer() - start) * 1000)
    except:
        logging.exception('exception occurred in fetch_worker()')
        stats.put(0)


class WSGIReloader(BaseReloader):
    def __init__(
            self, groups, htaccess, url=None, fetch_count=None,
            kill_signal=SIGTERM, group_format='(wsgi:%s)', **kwargs):
        super(WSGIReloader, self).__init__(**kwargs)
        self.groups = groups
        self.htaccess = htaccess
        self.url = url
        self.fetch_count = fetch_count
        self.kill_signal = kill_signal
        self.group_format = group_format

    def current_group(self):
        group = open(self.htaccess).read()
        group = group.replace('SetEnv PROCESS_GROUP', '').strip()
        enforce(group in self.groups, 'found invalid group %r' % group)
        return group

    def group_pids(self):
        name = self.group_format % self.current_group()
        items = get_pid_list()
        items = [(pid, process_name(pid, ignore_errors=True)) for pid in items]
        return [pid for pid, cmd in items if cmd and cmd[0].strip() == name]

    def kill_pids(self, pids):
        logging.info('killing pids %r' % pids)
        for i in pids:
            try:
                os.kill(i, self.kill_signal)
            except OSError as e:
                if e.errno != errno.ESRCH:  # ignore no such process errors
                    raise

    def fetch(self, proc_count):
        workers = []
        stats = []
        statsq = Queue()
        count = self.fetch_count or proc_count
        for i in range(count):
            worker = Thread(target=fetch_worker, args=(self.url, statsq))
            worker.start()
            workers.append(worker)
        for worker in workers:
            worker.join()
            stats.append(statsq.get())
        stats = ', '.join(["%dms" % i for i in sorted(stats, reverse=True)])
        logging.info('fetched %r with stats %s' % (self.url, stats))

    def reload(self):
        pids = self.group_pids()
        old = self.current_group()
        new = self.groups[(self.groups.index(old) + 1) % 2]
        logging.info('changing group from %r to %r' % (old, new))
        swap_save(self.htaccess, 'SetEnv PROCESS_GROUP %s\n' % new)
        if self.url:
            self.fetch(len(pids))
        self.kill_pids(pids)

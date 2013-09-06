
from watchdog.tricks import Trick
from itertools import cycle
from timeit import default_timer as timer
from signal import SIGTERM
from utile import get_pid_list, process_name
from threading import Thread
from Queue import Queue
from urllib import urlopen
import logging.config
import os
import errno

DEFAULT_LOGGING = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)5s - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
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


def fetch_worker(url, stats):
    start = timer()
    urlopen(url).read()
    stats.put((timer() - start) * 1000)


class ReloaderTrick(Trick):
    def __init__(
            self, groups, htaccess, fetch_url=None, fetch_count=0,
            log_config=None, wait=2, signal=SIGTERM, group_format='(wsgi:%s)',
            **kwargs):
        super(ReloaderTrick, self).__init__(**kwargs)
        log_config = log_config or DEFAULT_LOGGING
        logging.config.dictConfig(log_config)
        logging.info('ReloaderTrick started')
        self.groups = cycle(groups)
        self.current = next(self.groups)
        self.htaccess = htaccess
        self.wait = wait
        self.signal = signal
        self.fetch_url = fetch_url
        self.fetch_count = fetch_count
        self.group_format = group_format
        self.last_reload = 0
        self.fetch_stats = Queue()
        self.save_htaccess(self.current)

    def save_htaccess(self, group):
        logging.info('setting group to %r in %r' % (group, self.htaccess))
        with open(self.htaccess, 'w') as f:
            f.write('SetEnv PROCESS_GROUP %s\n' % group)

    def kill_group(self, group):
        name = self.group_format % group
        pids = []
        for pid in get_pid_list():
            try:
                cmd = process_name(pid)
            except IOError:
                continue
            if cmd and cmd[0].strip() == name:
                pids.append(pid)
        logging.info('killing %r with pids %r' % (name, pids))
        for i in pids:
            try:
                os.kill(i, self.signal)
            except OSError as e:
                if e.errno != errno.ESRCH:  # ignore no such process errors
                    raise

    def fetch(self):
        workers = []
        stats = []
        for i in range(self.fetch_count):
            args = (self.fetch_url, self.fetch_stats)
            worker = Thread(target=fetch_worker, args=args)
            worker.start()
            workers.append(worker)
        for worker in workers:
            worker.join()
            stats.append(self.fetch_stats.get())
        stats = ', '.join(["%dms" % i for i in sorted(stats)])
        logging.info('fetched %r with stats %s' % (self.fetch_url, stats))

    def on_any_event(self, event):
        if timer() - self.last_reload < self.wait:
            logging.info('ignored event %r' % event)
            return
        logging.info('reload event %r' % event)
        new = next(self.groups)
        self.save_htaccess(new)
        self.kill_group(self.current)
        self.fetch()
        self.fetch()
        self.current = new
        self.last_reload = timer()

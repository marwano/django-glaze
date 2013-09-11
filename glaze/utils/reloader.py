
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
import time

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


def fetch_worker(url, stats):
    try:
        start = timer()
        urlopen(url).read()
        stats.put((timer() - start) * 1000)
    except:
        logging.exception('exception occurred in fetch_worker()')
        stats.put(0)


class ReloaderTrick(Trick):
    def __init__(
            self, groups, htaccess, url=None, fetch_count=0, fetch_delay=0.1,
            log_config=None, ignore_period=1, signal=SIGTERM, group_format='(wsgi:%s)',
            **kwargs):
        super(ReloaderTrick, self).__init__(**kwargs)
        log_config = log_config or DEFAULT_LOGGING
        logging.config.dictConfig(log_config)
        logging.info('ReloaderTrick started')
        self.groups = cycle(groups)
        self.current = next(self.groups)
        self.htaccess = htaccess
        self.ignore_period = ignore_period
        self.signal = signal
        self.url = url
        self.fetch_count = fetch_count
        self.fetch_delay = fetch_delay
        self.group_format = group_format
        self.last_reload = 0
        self.proc_count = 0
        self.save_htaccess(self.current)

    def save_htaccess(self, group):
        logging.info('setting group to %r in %r' % (group, self.htaccess))
        with open(self.htaccess, 'w') as f:
            f.write('SetEnv PROCESS_GROUP %s\n' % group)

    def kill_group(self, group):
        name = self.group_format % group
        items = get_pid_list()
        items = [(pid, process_name(pid, ignore_errors=True)) for pid in items]
        pids = [pid for pid, cmd in items if cmd and cmd[0].strip() == name]
        self.proc_count = len(pids)
        if not pids:
            logging.error('no processes found with name %r' % name)
            return
        logging.info('killing %r with pids %r' % (name, pids))
        for i in pids:
            try:
                os.kill(i, self.signal)
            except OSError as e:
                if e.errno != errno.ESRCH:  # ignore no such process errors
                    raise

    def fetch(self):
        if self.fetch_delay:
            logging.info('sleeping for fetch delay of %ss' % self.fetch_delay)
            time.sleep(self.fetch_delay)
        workers = []
        stats = []
        statsq = Queue()
        count = self.fetch_count or self.proc_count
        for i in range(count):
            args = (self.url, statsq)
            worker = Thread(target=fetch_worker, args=args)
            worker.start()
            workers.append(worker)
        for worker in workers:
            worker.join()
            stats.append(statsq.get())
        stats = ', '.join(["%dms" % i for i in sorted(stats, reverse=True)])
        logging.info('fetched %r with stats %s' % (self.url, stats))

    def reload(self):
        new = next(self.groups)
        self.save_htaccess(new)
        self.kill_group(self.current)
        if self.url:
            self.fetch()
        self.current = new
        self.last_reload = timer()

    def on_any_event(self, event):
        if timer() - self.last_reload < self.ignore_period:
            logging.info('ignored event %r' % event)
        else:
            logging.info('reload event %r' % event)
            try:
                self.reload()
            except:
                logging.exception('exception occurred in reload()')
                raise

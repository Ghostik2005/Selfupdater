# coding: utf-8

__appname__ = 'autoreloader'
__version__ = '2017.208.1030' #using multiprocessing instead of threading
#__version__ = '2017.207.1730' #autoreloader

import os
import sys
import time
import shutil
import signal
import subprocess
import urllib.request
import multiprocessing
from itertools import chain

def _get_args_for_reloading():
    ret_val = [sys.executable,]
    ret_val.append(sys.argv[0])
    ret_val.extend(sys.argv[1:])
    return ret_val

def _get_params(update_path):
    for path in update_path:
        p_type = None
        _param = None
        if 'http' in path:
            try:
                with urllib.request.urlopen(path, timeout=2) as u_open:
                    if u_open.getcode() == 200:
                        _param = int(u_open.info()['Content-Length'])
                        p_type = 'url'
            except Exception as Err:
                #print('\n', Err, flush=True)
                pass
        else:
            try:
                _param = int(os.stat(path).st_size)
                p_type = 'local'
            except OSError:
                continue
        yield p_type, _param, path

class _reloader_class(object):
    _sleep = staticmethod(time.sleep)

    def __init__(self, update_path=None, interval=1):
        self.selfparam = int(os.stat(os.path.abspath(sys.argv[0])).st_size)
        self.update_path = update_path
        self.interval = interval

    def restart_with_reloader(self, pid):
        while True:
            print('\n--|Autoupdate and restart script', flush=True)
            args = _get_args_for_reloading()
            new_environ = os.environ.copy()
            new_environ['_MAIN'] = 'true'
            exit_code = subprocess.call(args, env=new_environ)
            if exit_code != 3:
                return exit_code

    def _reload(self, path_type, filename):
        f_path = os.path.abspath(sys.argv[0])
        new_fname = os.path.join(os.path.dirname(f_path), 'new_file.zip')
        if 'local' in path_type:
            shutil.copy2(filename, new_fname)
        else:
            with urllib.request.urlopen(filename, timeout=2) as u_open:
                if u_open.getcode() == 200:
                    data = u_open.read()
            with open(new_fname, 'wb') as f_open:
                f_open.write(data)
        old_fname = f'{f_path}.old'
        shutil.move(f_path, old_fname)
        shutil.move(new_fname, f_path)
        print('\n--|| file %r has been changed, reloading' % filename, flush=True)
        sys.exit(3)

    def run(self):
        compare_params = {}
        while True:
            for path_type, compare_param, filename in _get_params(self.update_path):
                if not path_type:
                    continue
                old_time = compare_params.get(filename, None)
                if not old_time:
                    compare_params[filename] = compare_param
                    continue
                elif compare_param != self.selfparam:
                    self._reload(path_type, filename)
            self._sleep(self.interval)

def run_reloader(main_func, update_path=None, interval=1):
    reloader = _reloader_class(update_path, interval)
    signal.signal(signal.SIGTERM, lambda *args: sys.exit(0))
    try:
        if os.environ.get('_MAIN') == 'true':
            multiprocessing.Process(target=main_func, args=(), daemon=True).start()
            reloader.run()
        else:
            sys.exit(reloader.restart_with_reloader(os.getpid()))
    except KeyboardInterrupt:
        print('\n', flush=True)
        print('Keyboard break, exiting...', flush=True)
    except Exception as Err:
        print(Err)
        sys.exit(0)


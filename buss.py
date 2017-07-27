# coding: utf-8
"""
main bussunes application
"""
import time

def f_main():
    c=0
    while True:
        c += 1
        time.sleep(1.5)
        print('main loop-->', c, end='\r', flush=True)



if __name__ == '__main__':
    """
    first argument - main bussines function,
    update_path - list of pathes for updates (local path (Linux-compatible or urls),
    interval - timeout for next update check
"""
    import _uploader as rl
    rl.run_reloader(
        f_main,
        update_path=[
                '/ms71/temp/upd.zip',
                'http://update.url',
            ],
        interval=5
    )

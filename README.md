What is Selfupdater?
====================

  Selfupdater is a small script, wrapping the main bussiness Python-writing application
and allows to get the new version of application from different sources. After
uploading of application, Selfupdater reload the main application.
  It works with pure python script and from zip-archived script.

What do I need?
===============

Selfupdater is run under Python 3.6 only.

Usage
===============

Here's one of the simplest applications you can make:

    def f_main():
        #main bussiness logic
       .
       .
       .
    if __name__ == '__main__':
       """
       first argument - main bussines function,
       update_path - list of paths for updates (local Linux-compatible paths  or urls),
       interval - timeout for next update check
       """
       import _updater as up
       up.run_reloader(
           f_main,
           update_path=[
                   '/ms71/temp/upd.zip',
                   'http://update.url/upd.zip',
               ],
           interval=5
       )

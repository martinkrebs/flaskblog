# flaskblog

## Create app and run locally
```
~/Code:$ mkdir flaskblog && cd flaskblog
~/Code/flaskblog:$
```

### Create python3 virtualenv of same name
```
~/Code/flaskblog:$ mkvirtualenv --python=$(which python3) flaskblog
Running virtualenv with interpreter /usr/local/bin/python3
Using base prefix '/usr/local/Cellar/python3/3.6.1/Frameworks/Python.framework/Versions/3.6'
New python executable in /Users/martinkrebs/.virtualenvs/flaskblog/bin/python3.6
Also creating executable in /Users/martinkrebs/.virtualenvs/flaskblog/bin/python
Installing setuptools, pip, wheel...done.
virtualenvwrapper.user_scripts creating /Users/martinkrebs/.virtualenvs/flaskblog/bin/predeactivate
virtualenvwrapper.user_scripts creating /Users/martinkrebs/.virtualenvs/flaskblog/bin/postdeactivate
virtualenvwrapper.user_scripts creating /Users/martinkrebs/.virtualenvs/flaskblog/bin/preactivate
virtualenvwrapper.user_scripts creating /Users/martinkrebs/.virtualenvs/flaskblog/bin/postactivate
virtualenvwrapper.user_scripts creating /Users/martinkrebs/.virtualenvs/flaskblog/bin/get_env_details
(flaskblog) ~/Code/flaskblog:$

```
> Remember to activate use: workon flaskblog, to stop use deactivate.

### Pip install flask and flake8 (flake8 used by atom ide)
```
(flaskblog) ~/Code/flaskblog:$ pip install flask flake8
...
```

### Create the file hello.py and add the following code
```
from flask import Flask


app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(port=5000, debug=True)
```

### Run with flask dev server from terminal
```
(flaskblog) ~/Code/flaskblog:$ python hello.py
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 238-149-146

```
- Look at the result in the browser at http://localhost:5000

---

## Deploy app to Linode.

### Technology stack
- Ubuntu 14.04 LTS
- Nginx
- uWSGI
- Python 3 and Flask

### Create required config files

```
# etc/init/uwsgi.conf
# No need to edit this file when adding new sites.

description "uWSGI application server in Emperor mode"

start on runlevel [2345]
stop on runlevel [!2345]


setuid martin
setgid www-data

exec /usr/local/bin/uwsgi --emperor /etc/uwsgi/sites
```

```
# /etc/uwsgi/sites/flaskblog.ini

[uwsgi]
project = flaskblog
base = /home/martin

chdir = %(base)/%(project)
home = %(base)/.virtualenvs/%(project)
module = wsgi
callable = app

master = true
processes = 5

socket = %(base)/%(project)/%(project).sock
chmod-socket = 664
vacuum = true

die-on-term = true
```

```
# /etc/nginx/sites-available/flaskblog

server {
    listen 80;
    server_name martintkrebs.com www.martintkrebs.com;

    location = /favicon.ico {access_log off; log_not_found off;}
    location /static/ {
        root /home/martin/flaskblog;
    }



    location / {
        include   	uwsgi_params;
        uwsgi_pass 	unix:/home/martin/flaskblog/flaskblog.sock;
    }
}
```

### Create a symlink
Create symlink from /etc/nginx/sites-available/yoursite to /etc/nginx/sites-enabled/yoursite
eg:

```
$ sudo ln -s /etc/nginx/sites-available/yoursite  /etc/nginx/sites-enabled/yoursite
```

### scp flaskblog code up to linode
```
~:$ scp -r ~/Code/flaskblog martin@martintkrebs.com:/home/martin
```
> Later we will use rsync with exclude-list.txt to specifiy what is uploaded.

### Edit the app.run() line in hello.py
Edit so the files app.run() is:
```
if __name__ == '__main__':
    app.run(host='0.0.0.0')
```
### Create a wsgi.py file
create file martin@callisto:~/flaskblog$ cat wsgi.py :
```
from hello import app


if __name__ == '__main__':
    app.run()
```

### Create a the virtualenv on Linode
$ mkvirtualenv --python=$(which python3) flaskblog

### pip install libs from requirements.txt
```
(flaskblog) martin@callisto:~/flaskblog$ pip install -r requirements.txt
```

### Start Nginx and uWSGI servers
```
(flaskblog) martin@callisto:~/flaskblog$ sudo service uwsgi start
uwsgi start/running, process 4436
(flaskblog) martin@callisto:~/flaskblog$ sudo service nginx start
(flaskblog) martin@callisto:~/flaskblog$
```

### View live page
The page should now be live on the web at:  http://www.martintkrebs.com

---

## rsync, a better upload alternative to scp

This will rsync a folder testdir and subcontents up to my Linode(mk:YES):
```
(flaskblog) ~:$ rsync -avz testdir martin@martintkrebs.com:/home/martin

```
rsync option -a indicates archive mode. -a option does the following,
- Recursive mode
- Preserves symbolic links
- Preserves permissions
- Preserves timestamp
- Preserves owner and group

v = verbose, z = compress whilst sending (this is uncompressed at the other end)

#### Use rsync ssh to enable the secured remote connection.
```
(mtkblog_dev) ~:$ rsync -avz -e ssh testdir martin@martintkrebs.com:/home/martin
```

#### Do Not Overwrite the Modified Files at the Destination
In a typical sync situation, if a file is modified at the destination,
we might not want to overwrite the file with the old file from the source.

Use rsync -u option to do exactly that. (i.e do not overwrite a file at the
destination, if it is modified).
```
rsync -avzu -e ssh testdir martin@martintkrebs.com:/home/martin
```

#### Exclude multiple files and directories at the same time

You can do this on the command line, or a better idea if you have lots of
folders/files to exclude is to list them in an exclude file and ref this
in your call to rsync:
```
(mtkblog_dev) ~:$ rsync -avz --exclude-from 'exclude-list.txt' -e ssh  testdir martin@martintkrebs.com:/home/martin

```
using this file: exclude-list.txt:
```
test.txt
test3.txt
subdir2
subdir/testsub.txt

```

#### only excludiing /.blahblah not any other .blahblah files. THIS WORKS:
```
sent 373 bytes  received 92 bytes  930.00 bytes/sec
total size is 85  speedup is 0.18
(mtkblog_dev) ~:$ rsync -avz --exclude "- /.blahblah" --dry-run  testdir/ martin@martintkrebs.com:/home/martin/testdir
building file list ... done
created directory /home/martin/testdir
./
test.txt
test2.txt
test3.txt
subdir/
subdir/.blahblah
subdir/testsub.txt
subdir/testsub2.txt
subdir/testsub3.txt
subdir2/
subdir2/testsubsub.txt

```

**It does not work if you do this:**
```
(mtkblog_dev) ~:$ rsync -avz --exclude "- /.blahblah" --dry-run  testdir martin@martintkrebs.com:/home/martin
```
> Thing work as you expect if you transfer from testdir/ ie the contents
of testdir over to /home/martin/testdir

> Use this form ... sourcdir/ --> /home/martin/sourcedir

> NOT this form: ... sourcdir --> /home/martin


#### rsync up to linode:
local command line in the flaskblog folder:
```
(flaskblog) ~:$ rsync -avzu -e ssh --exclude-from 'flaskblog-exclude.txt' flaskblog/ martin@martintkrebs.com:/home/martin/flaskblog
```


on linode:
- workon mtkblog
- migrate db
- collectstatic
- start or restart nginx and uwsgi

This should now work

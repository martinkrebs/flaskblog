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

from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def index():
    data = {'title': 'Hello from flaskblog!'}
    return render_template('index.html', data=data)


if __name__ == '__main__':
    app.run(port=5000, debug=True)

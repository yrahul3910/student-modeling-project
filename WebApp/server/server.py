from flask import Flask, send_from_directory
app = Flask(__name__, static_url_path='./dist')

@app.route('/')
def index():
    return app.send_static_file('index.html')
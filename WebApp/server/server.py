from flask import Flask, send_from_directory
import os

# Use the dist/ directory as the static files directory.
app = Flask(__name__,
            root_path=os.path.realpath(os.path.pardir) + '/WebApp',
            static_folder='dist',
            static_url_path='/')


@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def static_files(path):
    """
    Static files handler. / defaults to index.html, and the
    other files are matched via the expression.
    """
    return app.send_static_file(path)

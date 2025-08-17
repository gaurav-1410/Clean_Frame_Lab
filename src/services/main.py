from flask import Flask, render_template, request
import pandas as pd
from data_preview import upload_bp
from pre_processing import upload_pre_process

app = Flask(__name__, template_folder='../templates')

app.register_blueprint(upload_bp)
app.register_blueprint(upload_pre_process)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host= '0.0.0.0', debug=True)
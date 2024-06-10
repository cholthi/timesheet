#!/usr/bin/python3
""" Flask web application"""
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime
from flask import send_from_directory
from timesheet.main import generate

app = Flask(__name__)
app.config["UPLOAD_DIR"] = "static/docs/"
app.config['ROOT_PATH'] = app.root_path + '/' + app.config['UPLOAD_DIR']
app.config["OUTPUT_FILE"] = "For_Afrika_Staff_Timesheet.xlsx"
app.config['SECRET_KEY'] = 'rn4ury57874857'

date_format = "%m/%d/%Y"

@app.route('/')
def index():
    """ Index view"""
    print(app.root_path)
    return render_template('index.html')

@app.route('/timesheet/generate', methods=['POST'])
def generate_timesheet():
    """Generate and save timesheet on a web folder for later download"""
    f = request.files['timesheet']
    filename = secure_filename(f.filename)
    date = datetime.strptime(request.form.get('salary_date'), date_format)

    output_filename = f"{date.strftime('%b')}_{date.strftime('%d')}_{app.config['OUTPUT_FILE']}"
    input_file = app.config['ROOT_PATH'] + filename
    output_file = app.config['ROOT_PATH'] + output_filename 
    f.save(app.config['UPLOAD_DIR'] + filename)
    generate(input_file, output_file, date)
    flash("The file upload was successful. Please download the generated timesheet below")
    return redirect(url_for('get_download', filename=output_filename))

@app.route('/get_download', methods=['GET'])
def get_download():
    """ Render html page to download the timesheet"""
    return render_template('get_download.html', filename=request.args.get('filename'))

@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    """ download the generated timesheet view"""
    return send_from_directory(app.config['ROOT_PATH'], filename)



if __name__ == '__main__':
    app.run()

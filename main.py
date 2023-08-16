from flask import Flask, render_template, request, send_file
import subprocess
import os
import shutil
import zipfile

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('form.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    option = request.form['option']
    script_path = './script.py'
    cmd = ['python3', script_path, url, option]

    # run the script as a subprocess
    try:
        process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except subprocess.CalledProcessError as e:
        return render_template('error.html', error=e.stderr)

    # compress .pdf to .zip
    directory = '.'
    pdf_files = [f for f in os.listdir(directory) if f.endswith('.pdf')]
    zip_filename = 'marklist.zip'
    with zipfile.ZipFile(zip_filename, 'w') as zip_file:
        for pdf_file in pdf_files:
            file_path = os.path.join(directory, pdf_file)
            zip_file.write(file_path, pdf_file)

    # remove downloaded pdf files
    for file in pdf_files:
        file_path = os.path.join(directory, file)
        os.remove(file_path)

    # send .zip file for download
    try:
        return send_file(zip_filename, as_attachment=True, download_name='marklist.zip')
    finally:
        os.remove('marklist.zip')

if __name__ == '__main__':
    app.run()

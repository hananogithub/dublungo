import os
from flask import Flask, request, render_template, send_file, jsonify
from werkzeug.utils import secure_filename
import pandas as pd
import chardet

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

ALLOWED_EXTENSIONS = {'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
    return chardet.detect(raw_data)['encoding']

def align_texts(file1, file2):
    encoding1 = detect_encoding(file1)
    encoding2 = detect_encoding(file2)

    if encoding1 != 'utf-8' or encoding2 != 'utf-8':
        raise ValueError("Files must be UTF-8 encoded")

    with open(file1, 'r', encoding=encoding1) as f1, open(file2, 'r', encoding=encoding2) as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()

    if len(lines1) != len(lines2):
        raise ValueError("Files have different number of lines")

    df = pd.DataFrame({
        'Language 1': [line.strip() for line in lines1],
        'Language 2': [line.strip() for line in lines2]
    })

    output_file = 'translation_output.tsv'
    df.to_csv(output_file, sep='\t', index=False)
    return output_file

@app.route('/', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        if 'file1' not in request.files or 'file2' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file1 = request.files['file1']
        file2 = request.files['file2']
        if file1.filename == '' or file2.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        if file1 and allowed_file(file1.filename) and file2 and allowed_file(file2.filename):
            filename1 = secure_filename(file1.filename)
            filename2 = secure_filename(file2.filename)
            file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
            file2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
            try:
                output_file = align_texts(os.path.join(app.config['UPLOAD_FOLDER'], filename1),
                                          os.path.join(app.config['UPLOAD_FOLDER'], filename2))
                return jsonify({'success': True, 'file': output_file})
            except ValueError as e:
                return jsonify({'error': str(e)}), 400
        else:
            return jsonify({'error': 'File type not allowed'}), 400
    return render_template('upload.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
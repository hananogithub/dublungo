import os
from flask import Flask, request, render_template, send_file, jsonify
from werkzeug.utils import secure_filename
import pandas as pd
import chardet
from difflib import SequenceMatcher

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

def extract_text(file_path, encoding):
    with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
        return [line.strip() for line in f.readlines()]

def preprocess_texts(file1, file2):
    encoding1 = detect_encoding(file1)
    encoding2 = detect_encoding(file2)

    if encoding1 != 'utf-8' or encoding2 != 'utf-8':
        raise ValueError("Files must be UTF-8 encoded")

    # テキストを抽出
    text1 = extract_text(file1, encoding1)
    text2 = extract_text(file2, encoding2)

    return text1, text2

def align_texts(text1, text2):
    paired_lines = []
    used_indices = set()  # すでにペアになった行を記録

    for i, line1 in enumerate(text1):
        best_match_index = -1
        best_match_score = 0

        for j, line2 in enumerate(text2):
            if j in used_indices:
                continue  # すでにペアになった行はスキップ
            similarity = SequenceMatcher(None, line1, line2).ratio()
            if similarity > best_match_score:
                best_match_score = similarity
                best_match_index = j

        if best_match_score > 0.5:  # 類似度が0.5以上の場合にペアにする
            paired_lines.append((line1, text2[best_match_index]))
            used_indices.add(best_match_index)
        else:
            paired_lines.append((line1, ''))  # ペアが見つからない場合

    # ペアにならなかった行を追加
    for j, line2 in enumerate(text2):
        if j not in used_indices:
            paired_lines.append(('', line2))

    return paired_lines

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
                # 1つ目の処理: テキストを抽出
                text1, text2 = preprocess_texts(
                    os.path.join(app.config['UPLOAD_FOLDER'], filename1),
                    os.path.join(app.config['UPLOAD_FOLDER'], filename2)
                )

                # 2つ目の処理: テキストをペアリング
                paired_lines = align_texts(text1, text2)

                # 結果をTSVファイルに保存
                output_dir = os.path.join(app.root_path, 'static', 'outputs')
                os.makedirs(output_dir, exist_ok=True)
                output_file = os.path.join(output_dir, 'translation_output.tsv')
                df = pd.DataFrame(paired_lines, columns=['Language 1', 'Language 2'])
                df.to_csv(output_file, sep='\t', index=False)

                return jsonify({'success': True, 'file': os.path.join('static', 'outputs', 'translation_output.tsv')})
            except ValueError as e:
                return jsonify({'error': str(e)}), 400
        else:
            return jsonify({'error': 'File type not allowed'}), 400
    return render_template('upload.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.root_path, filename), as_attachment=True)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
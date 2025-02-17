from flask import Flask, request, send_file, jsonify
import os
import fitz  # PyMuPDF for PDF processing
import spacy

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Load NLP model
nlp = spacy.load("en_core_web_sm")

@app.route("/upload", methods=["POST"])
def upload_files():
    if "file1" not in request.files or "file2" not in request.files:
        return jsonify({"error": "Both files are required"}), 400
    
    file1 = request.files["file1"]
    file2 = request.files["file2"]
    
    path1 = os.path.join(UPLOAD_FOLDER, file1.filename)
    path2 = os.path.join(UPLOAD_FOLDER, file2.filename)
    file1.save(path1)
    file2.save(path2)
    
    text1 = extract_text(path1)
    text2 = extract_text(path2)
    
    aligned_text = align_texts(text1, text2)
    output_path = save_aligned_text(aligned_text)
    
    return jsonify({"success": True, "file": output_path})

def extract_text(filepath):
    ext = os.path.splitext(filepath)[-1].lower()
    
    if ext == ".pdf":
        doc = fitz.open(filepath)
        text = "\n".join([page.get_text("text") for page in doc])
    else:
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
    return text

def align_texts(text1, text2):
    lines1 = text1.split("\n")
    lines2 = text2.split("\n")
    min_len = min(len(lines1), len(lines2))
    aligned = [f"{lines1[i]} ||| {lines2[i]}" for i in range(min_len)]
    return "\n".join(aligned)

def save_aligned_text(aligned_text):
    output_path = os.path.join(OUTPUT_FOLDER, "aligned_output.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(aligned_text)
    return output_path

@app.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    file_path = os.path.join(OUTPUT_FOLDER, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({"error": "File not found"}), 404

if __name__ == "__main__":
    app.run(debug=True, port=5000)

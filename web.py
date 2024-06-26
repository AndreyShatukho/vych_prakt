from flask import Flask, render_template, request
import Levenshtein
import re

def normalize_code(code):
    normalized_code = re.sub(r'\b[a-zA-Z_]\w*\b', 'VAR_NAME', code)
    return normalized_code

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check_plagiarism():
    file1 = request.files['file1']
    file2 = request.files['file2']

    code1 = file1.read().decode('utf-8')
    code2 = file2.read().decode('utf-8')

    normalized_code1 = normalize_code(code1)
    normalized_code2 = normalize_code(code2)

    distance = Levenshtein.distance(normalized_code1, normalized_code2)
    similarity = (1 - (distance / max(len(normalized_code1), len(normalized_code2)))) * 100

    return render_template('result.html', similarity=similarity)

if __name__ == '__main__':
    app.run()
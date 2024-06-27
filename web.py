from flask import Flask, render_template, request
import Levenshtein
import re

def normalize(code):
    normalized_code = re.sub(r'\b[a-zA-Z_]\w*\b', 'VAR_NAME', code)
    return normalized_code

def find_similar_lines(code1, code2, original_code1, original_code2):
    lines1 = code1.split('\n')
    lines2 = code2.split('\n')

    similar_lines = []

    for line1, original_line1 in zip(lines1, original_code1.split('\n')):
        for line2, original_line2 in zip(lines2, original_code2.split('\n')):
            stripped_line1 = line1.strip()
            stripped_line2 = line2.strip()

            if stripped_line1 and stripped_line2 and stripped_line1 == stripped_line2:
                similar_lines.append((original_line1, original_line2))

    return similar_lines

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

    normalized1 = normalize(code1)
    normalized2 = normalize(code2)

    distance = Levenshtein.distance(normalized1, normalized2)
    similarity = (1 - (distance / max(len(normalized1), len(normalized2)))) * 100
    similar_lines = find_similar_lines(normalized1, normalized2, code1, code2)

    return render_template('result.html', similarity=similarity, similar_lines=similar_lines)

if __name__ == '__main__':
    app.run()

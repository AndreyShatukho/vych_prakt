from flask import Flask, render_template, request
import Levenshtein

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

    distance = Levenshtein.distance(code1, code2)
    similarity = (1 - (distance / max(len(code1), len(code2)))) * 100

    return render_template('result.html', similarity=similarity)

if __name__ == '__main__':
    app.run()

from flask import Flask, render_template, request
import ast
import Levenshtein

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_plagiarism', methods=['POST'])
def check_plagiarism():
    file1 = request.files['file1']
    file2 = request.files['file2']

    code1 = file1.read().decode('utf-8')
    code2 = file2.read().decode('utf-8')

    distance = Levenshtein.distance(code1, code2)
    similarity = (1 - (distance / max(len(code1), len(code2)))) * 100

    try:
        tree1 = ast.parse(code1)
        tree2 = ast.parse(code2)
    except SyntaxError as e:
        return render_template('result.html', error_message='Ошибки синтаксиса в одном или обоих файлах.')

    ast_str1 = ast.dump(tree1)
    ast_str2 = ast.dump(tree2)

    return render_template('result.html', similarity=similarity, ast_str1=ast_str1, ast_str2=ast_str2)

if __name__ == '__main__':
    app.run()
from flask import Flask, render_template, request
import Levenshtein
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def remove_comments(code):
    code = re.sub(r'\/\/.*', '', code)
    code = re.sub(r'\/\*(.|\n)*?\*\/', '', code)
    return code

def normalize(code):
    code = remove_comments(code)
    lines = code.split('\n')
    filtered = [line for line in lines if not line.startswith('import') and not line.startswith('from')]
    normalized_code = '\n'.join(filtered)
    normalized_code = re.sub(r'\b[a-zA-Z_]\w*\b', 'VAR_NAME', normalized_code)
    return normalized_code, filtered

def find_similar_lines(code1, code2, original_code1, original_code2):
    lines1 = code1.split('\n')
    lines2 = code2.split('\n')

    similar_lines = []

    for line1, original_line1 in zip(lines1, original_code1):
        for line2, original_line2 in zip(lines2, original_code2):
            stripped_line1 = line1.strip()
            stripped_line2 = line2.strip()

            if stripped_line1 and stripped_line2 and stripped_line1 == stripped_line2:
                similar_lines.append((original_line1, original_line2))

    return similar_lines

def calculate_similarity_leven(code1, code2):
    distance = Levenshtein.distance(code1, code2)
    similarity = (1 - (distance / max(len(code1), len(code2)))) * 100
    return similarity

def calculate_similarity_cosine(code1, code2):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([code1, code2])
    similarity_matrix = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])
    similarity = similarity_matrix[0][0] * 100
    return similarity

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
    normalized1, normalized11 = normalize(code1)
    normalized2, normalized21 = normalize(code2)

    similarity_leven = calculate_similarity_leven(normalized1, normalized2)
    similarity_cosine = calculate_similarity_cosine(normalized1, normalized2)
    similar_lines = find_similar_lines(normalized1, normalized2, normalized11, normalized21)

    return render_template('result.html', similarity_leven=similarity_leven, similarity_cosine=similarity_cosine, similar_lines=similar_lines)

if __name__ == '__main__':
    app.run()

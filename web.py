from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import Levenshtein
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from func import remove_comments, normalize,find_similar_lines, calculate_similarity_leven, calculate_similarity_cosine

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

    show_image = similarity_cosine > 70

    return render_template('result.html', similarity_leven=similarity_leven, similarity_cosine=similarity_cosine,
                           similar_lines=similar_lines, show_image=show_image)

@app.route("/image.jpg")
def image():
    return render_template("image.jpg")

if __name__ == '__main__':
    app.run(port=65)
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
import difflib

def convert_to_html(input_file):
    output_file = input_file[:-3] + ".html"

    with open(input_file, "r") as file:
        code = file.read()

    lexer = PythonLexer()
    formatter = HtmlFormatter(style="colorful")

    highlighted_code = highlight(code, lexer, formatter)

    with open(output_file, "w") as file:
        file.write(highlighted_code)

def compare_files(file1, file2):
    with open(file1, "r") as file:
        html1 = file.readlines()

    with open(file2, "r") as file:
        html2 = file.readlines()

    diff = difflib.SequenceMatcher(None, html1, html2)
    similarity = diff.ratio()

    return similarity/100

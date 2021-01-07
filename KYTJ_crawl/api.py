from flask import Flask, request, jsonify

from .db import university_db


app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def main():
    universities = university_db.get_universities()
    if request.method == 'POST':
        return jsonify([dict(x) for x in universities])
    else:
        res_text = """<table border="1" width=780px align="center" 
            height = 200px cellspacing=0 bordercolor=#FBBF00>{}</table>"""       
        _r = ""
        for x in universities:
            tr = "<tr>{}</tr>"
            tds = "".join(["<td>%s</td>"%j for i, j in enumerate(x) if i !=2])
            _r += tr.format(tds)
        return res_text.format(_r)

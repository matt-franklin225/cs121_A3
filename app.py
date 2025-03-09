from flask import render_template, request, Flask, jsonify
from search import search_from_query

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search", methods= ['GET'])
def search():
    query = request.args.get("query", "").lower()
    results = search_from_query(query)

    return jsonify(results=results)

if __name__ == "__main__":
    app.run(debug=True)

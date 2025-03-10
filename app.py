from flask import render_template, request, Flask
from search import search_from_query
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

stemmer = PorterStemmer()

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search", methods= ['GET'])
def search():
    query_str = request.args.get("query", "").lower()
    if query_str:
        query_str = word_tokenize(query_str)
        query = [token for token in query_str if token.isalnum()]
        stems = [stemmer.stem(token) for token in query if token.isalnum()]
        results = search_from_query(stems)
        if results:
            return render_template("result.html", query=query, results=results)
        else:
            return "No results found--please try a different query."
    else:
        # print("no query")
        return "You have not entered a query, please try again."

if __name__ == "__main__":
    app.run(debug=True)
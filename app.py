from flask import Flask, render_template, request
import json
import random

app = Flask(__name__)

# Load books
with open("books.json", "r", encoding="utf-8") as f:
    library = json.load(f)

# Extract unique tags
available_tags = sorted({tag for book in library for tag in book["tags"]})

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", available_tags=available_tags)

@app.route("/recommend", methods=["POST"])
def recommend():
    # Get selected tags
    user_tags = request.form.getlist("tags")
    user_tags = [t.lower() for t in user_tags]

    if not user_tags:
        error = "Please select at least one tag."
        return render_template("index.html", error=error, available_tags=available_tags)

    # Count matching tags
    recommendations = []
    for book in library:
        matches = len(set([t.lower() for t in book["tags"]]) & set(user_tags))
        if matches > 0:
            recommendations.append((matches, random.random(), book))  # random tie-breaker

    # Sort by matches descending, shuffle ties
    recommendations.sort(key=lambda x: (x[0], x[1]), reverse=True)
    top_books = [b for _, _, b in recommendations][:5]

    return render_template("recommendations.html", user_tags=user_tags, recommendations=top_books)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

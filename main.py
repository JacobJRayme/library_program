from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

all_books = []


@app.route('/')
def home():
    list_of_strings = []
    for book in all_books:
        list_of_strings.append(f"{book['title']} - {book['author']} - {book['rating']}")
    print(list_of_strings)
    return render_template('index.html', books=list_of_strings)


@app.route("/add", methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        new_dict = {
            "title": request.form['title'],
            "author": request.form['author'],
            "rating": request.form['rating']
        }
        print(new_dict)
        all_books.append(new_dict)
    return render_template('add.html')


if __name__ == "__main__":
    app.run(debug=True)
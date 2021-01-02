from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'  {self.title} - {self.author} - {self.rating}/10  '


# db.create_all()
#
# #CREATE RECORD
# new_book = Book(title="YES", author="YES", rating=9.3)
# db.session.add(new_book)
# db.session.commit()


@app.route('/')
def home():
    all_books = db.session.query(Book).all()
    return render_template('index.html', books=all_books)


@app.route('/delete/<int:id>', methods=['GET', 'DELETE'])
def delete(id):
    book_to_delete = Book.query.get(id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/add", methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        new_dict = {
            "title": request.form['title'],
            "author": request.form['author'],
            "rating": float(request.form['rating'])
        }
        print(new_dict)
        new_book = Book(title=new_dict["title"], author=new_dict["author"], rating=new_dict["rating"])
        db.session.add(new_book)
        db.session.commit()
    return render_template('add.html')


@app.route("/edit/<int:id>", methods=['POST', 'GET'])
def edit(id):
    if request.method == 'POST':
        new_ranking = request.form['ranking']
        book = Book.query.get(id)
        book.rating = new_ranking
        db.session.commit()
        print("They hit submit")
        return redirect(url_for('home'))
    book_to_update = Book.query.get(id)
    print(f"{book_to_update} is the book I want to update")
    return render_template('edit.html', book=book_to_update)


if __name__ == "__main__":
    app.run(debug=True)

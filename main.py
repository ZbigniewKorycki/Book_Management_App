from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#add database under directory instance i.e. ./instance/books-database.db
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books-database.db"

db = SQLAlchemy(app)


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.VARCHAR(250), nullable=False, unique=True)
    author = db.Column(db.VARCHAR(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Book {self.title}>"


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    with app.app_context():
        all_books = Books.query.all()
    return render_template("index.html", books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        with app.app_context():
            new_book = Books(
                title=request.form["title"],
                author=request.form["author"],
                rating=float(request.form["rating"]),
            )
            db.session.add(new_book)
            db.session.commit()
        return redirect(url_for("home"))
    return render_template("add.html")


@app.route("/edit", methods=["POST", "GET"])
def edit():
    if request.method == "POST":
        book_id = request.form["id"]
        book_to_update = db.get_or_404(Books, book_id)
        book_to_update.rating = request.form["updated_rating"]
        db.session.commit()
        return redirect(url_for("home"))
    book_id = request.args.get("id")
    book_selected = db.get_or_404(Books, book_id)
    return render_template("editor.html", book=book_selected)


@app.route("/delete", methods=["GET"])
def delete():
    book_id = request.args.get("id")
    book_to_delete = db.session.execute(
        db.select(Books).where(Books.id == book_id)
    ).scalar()
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)

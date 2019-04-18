import os

from flask import Flask, session, flash, request, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import render_template, redirect, url_for
from functools import wraps
from flask import g
import requests, json


app = Flask(__name__)
#engine = "postgres://obzimppmxvagjv:6a750aaf850171c69c54cd3b4b6623c5ec352299dfa8e16367a0507634cb195a@ec2-54-235-156-60.compute-1.amazonaws.com:5432/d58h5g292jours"
# Check for environment variable

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

    # Registering a user
@app.route("/register", methods=["POST","GET"])
def register():
    if request.method == "POST":
        #get form fields
        name = request.form.get("name")
        password = request.form.get("password")
        confirmPassword = request.form.get("confirmPassword")
        users = db.execute("SELECT * FROM users").fetchall()
# check if password is the same
        if password != confirmPassword:
            flash("Password does not match", "danger")
            return redirect(url_for("register"))
            # check if username is available
        elif db.execute("SELECT * FROM users WHERE name = :name", {"name": name}).rowcount:
            flash("The username has been taken, Try New username", "danger")
            return redirect(url_for("register"))
            # if all passed register user
        else:
            db.execute("INSERT INTO users(name, password) VALUES (:name,  :password)",{"name": name, "password": password})
            db.commit()
            flash('You are successfully registered, please login below!', 'success')
        return redirect(url_for("login"))
    return render_template("register.html")

#login route and function
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")

        user = db.execute("SELECT * FROM users WHERE (name ='" + name + "') AND (password = '" + password + "')").first()
        if user:
            session["name"] = user.name
            session["logged_in"] = True
            return redirect(url_for("dashboard"))
            flash("Successfully logged in", "success")
        else:
            error = "Invalid login credentials"
            return render_template("login.html", error=error)

    return render_template("login.html", invalid=True)
# login decoratr to check f user if logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        #logged in logic from session setting
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("Right place but wrong entrants, please login", "danger")
            return redirect(url_for("login"))
    return decorated_function

# clear session/ logout the user

@app.route("/logout")
def logout():
    session.clear()
    flash("Goodbye, Happy reading!", "success")
    return redirect(url_for("index"))
# Index Page / landing page
@app.route("/")
def index():
    books = db.execute("SELECT * FROM books ORDER BY year DESC LIMIT 3").fetchall()
    old = db.execute("SELECT * FROM books ORDER BY year ASC LIMIT 3").fetchall()
    return render_template("index.html",books=books, old=old)
#display books on Nav
@app.route("/books", methods=["GET", "POST"])
@login_required
def books():
    books = db.execute("SELECT * FROM books").fetchall()
    return render_template("books.html", books=books)

@app.route("/isbn/<string:isbn>", methods=["POST", "GET"])
#decorator to check if the user is logged in
@login_required
def book(isbn):
    name=session.get('name')
    # creating reviews session
    session["reviews"]=[]
    if request.method == "POST":
        rating = request.form.get("rating")
        message = request.form.get("message")

       # making sure that one review per book per user

        if db.execute("SELECT * FROM reviews WHERE (isbn ='" + isbn + "') AND (name = '" + name + "')").first():
            flash("You can only leave one review per book,Please choose another book below!", "danger")
            return redirect(url_for("books"))
        else:
             db.execute("INSERT INTO reviews (rating, message, isbn, name) VALUES (:rating, :message, :isbn, :name)", {"rating":rating, "message": message, "isbn":isbn, "name": name})
             db.commit()
             flash("Review submitted successfully, Check your dashboard for all your reviewed books!", "success")
        return redirect(url_for("books"))

    # Fetch Goodreads data with API
    res = requests.get("https://www.goodreads.com/book/review_counts.json/", params={"key":"nyl5lAQETqTmqyKtHcULRA", "isbns": isbn})
    if res.status_code !=200:
        return jsonify({"ERROR": "No such book or ISBN found."}),422
    work_ratings_count= res.json()['books'][0]['work_ratings_count']
    average_rating =res.json()['books'][0]['average_rating']
  # making sure book exist
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn",{"isbn":isbn}).fetchone()
    reviews = db.execute("SELECT * FROM reviews WHERE isbn = :isbn",{"isbn":isbn}).fetchall()
    for x in reviews:
        session['reviews'].append(x)
    return render_template("book.html", name=name,work_ratings_count=work_ratings_count,average_rating=average_rating,book=book,reviews=session['reviews'])
# local api
@app.route("/api/book/<string:isbn>")
def api(isbn):
    rating = []
    total = "No reviews."
    average_score = "No reviews."
    messages = []
    # check if book exist
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    if book is None:
        return jsonify({"error": "Invalid ISBN"}), 422
    reviews = db.execute("SELECT * FROM reviews").fetchall()
    for review_message in reviews:
        messages.append(review_message.message)
        # fetching reviews from reviews db
    total_reviews = db.execute("SELECT  FROM reviews WHERE isbn =:isbn",{"isbn":isbn}).fetchall()
    if total_reviews is None:
        total
        average_score
    else:
        total = len(total_reviews)
        score = db.execute("SELECT  FROM reviews WHERE isbn =:isbn",{"isbn":isbn}).fetchall()
    # returns json results for api
    return jsonify({
        "title": book.title,
        "author": book.author,
        "isbn": book.isbn,
        "year": book.year,
        "review_count": total,
        "messages": messages
    })
# search bar
@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    session["books"]=[]
    if request.method=="POST":
        text=request.form.get('text')
        # searching variety of results from books db
        results=db.execute("SELECT * FROM books WHERE author iLIKE '%"+text+"%' OR title iLIKE '%"+text+"%' OR isbn iLIKE '%"+text+"%'").fetchall()
        for search in results:
            session['books'].append(search)
        if len(session["books"])==0:
            flash("Book not found. Browse Available Books Menu for More Books.", "danger")
    return render_template("search.html",results=session['books'])
# user dashboard
@app.route("/dashboard", methods=["GET", "POST"])
@login_required # guard
def dashboard():
    name=session.get('name')
    personalReviews = db.execute("SELECT * FROM reviews  WHERE name=:name ORDER BY review_date DESC", {"name":name}).fetchall()
    otherUsers_Reviews = db.execute("SELECT * FROM reviews WHERE name!=:name ORDER BY review_date DESC", {"name":name}).fetchall()
    recommended = db.execute("SELECT *  FROM books WHERE year>= 1599 AND year < 1872 ORDER BY year DESC LIMIT 6").fetchall()

    return render_template("dashboard.html", personalReviews=personalReviews, book=book, otherUsers_Reviews =otherUsers_Reviews, recommended=recommended)

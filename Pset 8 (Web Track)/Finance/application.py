import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    purchases = db.execute("SELECT * FROM shares WHERE user_id = :user_id", user_id=session["user_id"])
    for purchase in purchases:
        purchase["currentPrice"] = lookup(purchase["symbol"])["price"]
        purchase["totalValue"] = purchase["currentPrice"] * purchase["number"]
    balance = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
    return render_template("index.html", rows=purchases, balance=balance)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")
    else:
        symbol = request.form.get("quote")
        shares = int(request.form.get("shares"))
        if not symbol:
            return apology("You haven't entered a quote!")
        if not shares:
            return apology("You haven't entered shares number!")
        if int(shares) < 0:
            return apology("Shares can't be negative")
        quote = lookup(symbol)
        if quote == None:
            return apology("Symbol does not exist")
        price = quote["price"]
        name = quote["name"]
        symbol = quote["symbol"]
        totalPrice = float(price) * int(shares)
        cash = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])[0]["cash"]
        if (cash < totalPrice):
            return apology("You can't afford these shares")
        db.execute("UPDATE users SET cash = cash - :totalPrice Where id = :id", totalPrice=totalPrice, id=session["user_id"])
        x = db.execute("SELECT symbol FROM shares WHERE user_id= :user_id", user_id=session["user_id"])
        for i in x:
            if symbol == i["symbol"]:
                db.execute("UPDATE shares SET number = number + :n WHERE user_id = :user_id AND symbol = :symbol", n=shares, user_id=session["user_id"], symbol=symbol)
                break
        else:
            db.execute("INSERT INTO shares (user_id, symbol, number, currentPrice, totalValue) VALUES (:user_id, :symbol, :number, :currentPrice, :totalValue)", user_id=session["user_id"], symbol=symbol, number=shares, currentPrice=0, totalValue=0)

        db.execute("INSERT INTO transactions (user_id, symbol, number, price) VALUES (?, ?, ?, ?)", session["user_id"], symbol, int(shares), price)
        return redirect("/")



@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transaction = db.execute("SELECT * FROM transactions WHERE user_id = :user_id ORDER BY time DESC", user_id = session["user_id"])
    return render_template("history.html", rows=transaction)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")
    else:
        symbol = request.form.get("quote")
        quote = lookup(symbol)
        if quote == None:
            return apology("Symbol does not exist")
        return render_template("quoteInfo.html", name=quote["name"], symbol=quote["symbol"], price=quote["price"])


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
         # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        elif not request.form.get("passwordConfirm"):
            return apology("must provide password confirmation", 403)

        else:
            # Query database for username
            rows = db.execute("SELECT * FROM users WHERE username = :username",
                              username=request.form.get("username"))

            # Ensure username exists and password is correct
            if len(rows) > 0:
                return apology("Username is already taken", 403)

            if (request.form.get("password") != request.form.get("passwordConfirm")):
                return apology("Password confirmation does not match")

            db.execute("INSERT INTO users (username, hash) VALUES (:username, :hashVal)", username=request.form.get("username"), hashVal=generate_password_hash(request.form.get("password")))

            # Redirect user to home page
            return redirect("/login")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        purchases = db.execute("SELECT symbol FROM shares WHERE user_id = :user_id", user_id = session["user_id"])
        return render_template("sell.html", purchases=purchases)
    else:
        if not request.form.get("purchase"):
            return apology("You have to select a purchase symbol")
        if not request.form.get("shares"):
            return apology("You have to specify the number of shares")
        if int(request.form.get("shares")) < 0:
            return apology("Shares can't be negative")
        purchase = request.form.get("purchase")
        shares = int(request.form.get("shares"))
        userShares = db.execute("SELECT * from shares WHERE user_id = :user_id", user_id = session["user_id"])
        for share in userShares:
            if purchase == share["symbol"]:
                if int(share["number"]) < int(shares):
                    return apology("You don't have that much shares!")
                else:
                    db.execute("UPDATE shares SET number = number - :shares WHERE user_id = :user_id AND symbol = :symbol", shares=shares, user_id=session["user_id"], symbol=purchase)
                break
        currentPrice = lookup(purchase)["price"]
        db.execute("UPDATE users SET cash = cash + :val WHERE id = :id", val = float(currentPrice) * int(shares), id=session["user_id"])

        db.execute("INSERT INTO transactions (user_id, symbol, number, price) VALUES (?, ?, ?, ?)", session["user_id"], purchase, -1 * int(shares), currentPrice)
        return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

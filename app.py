from flask import Flask
from flask_session import Session
from flask import render_template, url_for, redirect, g, session, request
from werkzeug.security import check_password_hash, generate_password_hash
from database import get_db, close_db
from datetime import datetime
from forms import LoginForm, RegistrationForm, MessageForm, ProfileForm
from functools import wraps


app = Flask(__name__)
app.teardown_appcontext(close_db)
app.config["SECRET_KEY"] = "i-never-attend-labs"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#The land page
@app.route("/")
def index():
    return render_template("index.html", header = "Welcome to Blender")

@app.before_request
def load_logged_in_user():
    g.user = session.get("user_id", None)


# Registration
@app.route("/register", methods = ["GET", "POST"])
def register():


    form = RegistrationForm()
    if form.validate_on_submit():
        userid = form.userid.data
        password = form.password.data
        password2 = form.password2.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        age = form.age.data
        gender = form.gender.data
        # i originally tried doing datetime now minus the datetime the user enters but it wouldn't work
        #despite the fact that it worked just fine in replit.
        # so i ended up doing this weird af conversion
        today = datetime.now().date()
        def to_integer(dt_time):
          return 10000 * dt_time.year + 100 * dt_time.month + dt_time.day


        ageInt = to_integer(age)
        todayInt = to_integer(today)
        n = todayInt - ageInt
        nw = n / 10000

       
    
        


        if age >= datetime.now().date():
            form.age.errors.append("Date must be in the past")
        elif nw < 18:
            form.age.errors.append("You must be 18 to join!")
        else:
            db = get_db()
            existinguser = db.execute("""SELECT * FROM users WHERE user_id = ?;""", (userid,)).fetchone()
            if existinguser is not None:
                form.userid.errors.append("User ID taken")
            else:
                db.execute("""INSERT INTO users (user_id, password, first_name, last_name, age, gender)
                VALUES (?, ?, ?, ?, ?, ?);""", (userid, generate_password_hash(password), first_name, last_name, age, gender))
                db.commit()
                return redirect(url_for("login"))
    return render_template("register.html", form = form)

# Login
@app.route("/login", methods = ["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        userid = form.userid.data
        password = form.password.data
        db = get_db()
        existinguser = db.execute("""SELECT * FROM users WHERE user_id = ?;""", (userid,)).fetchone()
        if existinguser is None:
            form.userid.errors.append("This User ID is not registered")
        elif not check_password_hash(existinguser["password"], password):
            form.password.errors.append("Incorrect password!")
        else:
            session.clear()
            session["user_id"] = userid
            next_page = request.args.get("next")
            if not next_page:
                next_page = url_for("landing")
            return redirect(next_page)
    return render_template("login.html", form = form)


# if user isn't logged in, this function redirects to login page
def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("login", next = request.url))
        return view(**kwargs)
    return wrapped_view

# Dashboard for users user
@app.route("/landing")
@login_required
def landing():
    user = session.get("user_id", None)
    return render_template("landing.html", header = "Dashboard", user = user)

# log out function
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

# User Profiles
@app.route("/profile/<user_id>", methods=["GET", "POST"])
@login_required
def profile(user_id):
    visitor = session.get("user_id", None)
    
    db = get_db()
    info = db.execute("""SELECT user_id, first_name, age, gender FROM users 
        WHERE user_id = ?;""", [user_id]).fetchall()
    db = get_db()
    bios = db.execute("""SELECT bio FROM bios WHERE 
        bio_id = ?
        ORDER BY b_id DESC;""", 
        [user_id]).fetchone()
    bios = bios
    if user_id == visitor:
        db = get_db()
        form = ProfileForm()
        if form.validate_on_submit():
            bio = form.bio.data
            bio_id = user_id
            db = get_db()
            
            db.execute("""INSERT INTO bios (bio_id, bio)
            VALUES (?, ?);""", (bio_id, bio))
            db.commit()
        return render_template("edit_profile.html", form = form, info = info, bios = bios)
    else:
        return render_template("profile.html", info = info, bios = bios)

# List of all users
@app.route("/users/", methods = ["GET", "POST"])
@login_required
def users():
    user_id = session.get("user_id", None)
    db = get_db()
    users = db.execute("""SELECT user_id, first_name, age, gender FROM users 
        WHERE user_id IS NOT ?;""", [user_id]).fetchall()

    return render_template("users.html", users = users)


# route to allow access to all database messages ass well as sending to db
@app.route("/chat/<user_id>", methods = ["GET", "POST"])
@login_required
def chat(user_id):
    form = MessageForm()
    sender_id = session.get("user_id", None)
    if sender_id == user_id:
        return redirect(url_for("landing"))
    else:
        db = get_db()
        msgs =reverse(db.execute("""SELECT * FROM messages WHERE 
            (sender_id = ? AND receiver_id = ?) OR (sender_id = ? AND receiver_id = ?)
            ORDER BY id DESC LIMIT 10;""", 
            (user_id, sender_id, sender_id, user_id)).fetchall())
        if form.validate_on_submit():
            receiver_id = user_id
            message = form.message.data
            sent = ""
            db = get_db()
            db.execute("""INSERT INTO messages (sender_id, receiver_id, message)
                VALUES (?, ?, ?);""", (sender_id, receiver_id, message))
            db.commit()
            return redirect(url_for("chat", user_id = user_id))

        return render_template("chat.html", caption="Chat", form = form, sender_id = sender_id, msgs = msgs)

# to flip messages
def reverse(list):
    l = [None]*len(list)
    for i in range(len(list)):
        l[len(list)-i-1] = list[i]
    return l
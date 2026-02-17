from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import re

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("blog.db")
    conn.row_factory = sqlite3.Row
    return conn

def sanitize(text:str):
    if text.isdigit():
        return True
        # Common malicious patterns (can be expanded)
    suspicious_patterns = [
        r"<[^>]*>",         # HTML tags
        r"(javascript:)",   # JavaScript URI
        r"--",              # SQL comment
        r"(?i)\b(SELECT|INSERT|UPDATE|DROP|SCRIPT|ALERT)\b",  # SQL/JS keywords
    ]
    for pattern in suspicious_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return False  
    return True  



@app.before_request
def middleware_forms():
    print("Checking the input before processing")
    methods = ["GET","PUT","POST","PATCH","DELETE"]
    if request.method in methods : 
        print(request.form)
        for key,val in request.form.items():

            print(key,val)
            if not sanitize(val):
                print("Redirecting to home")
                return redirect(url_for("home"))
            

@app.route("/")
def home():
    db = get_db()
    posts = db.execute("SELECT * FROM posts ORDER BY id DESC").fetchall()
    
    return render_template("index.html", title="Home Page",posts = posts)

@app.route("/login", methods=["GET","POST"])
def login():
    # Extract from the form input data
    if request.method == "POST":
        print(request.form)
        username = request.form.get("username")
        password = request.form.get("password")

        # Check input
        if not username and not password:
            return render_template("login.html",error="Missing username or password")
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username =  ? AND password = ?",(username,password)).fetchone()
        if user:
            return redirect(url_for("home"))
        else : 
            return render_template("login.html",error="Invalid credentials")

    return render_template("login.html")

@app.route("/signup", methods=["GET","POST"])
def signup():
    # Extract from the form input data
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
         # Check input
        if not username or not password:
            return render_template("signup.html",error="Missing username or password")
        
        # Check if user already exists
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username =  ?",(username,)).fetchone()
        if user:
            return render_template("signup.html",error="Username already exists")
        
        # Create the user
        db.execute("INSERT INTO users (username,password) VALUES (?,?)",(username,password))
        db.commit()
        return redirect(url_for("login"))
    
    return render_template("signup.html")


@app.route("/update-profile", methods=["GET","POST"])
def update_profile():
    if request.method == "POST":
        method_override = request.form.get("_method")
        if method_override == "PUT":
            username = request.form.get("username")
            new_password = request.form.get("new_password")

            db = get_db()
            user = db.execute("SELECT * FROM users WHERE username =  ?",(username,)).fetchone()
            if not user:
                return render_template("update_profile.html",error="User Not Found")
            
            if not new_password:
                return render_template("update_profile.html",error="Missing New Password")
            
            db.execute("UPDATE users SET password = ? WHERE username = ?",(new_password,username))
            db.commit()
            return render_template("update_profile.html",message="Password updated successfully")
        
    return render_template("update_profile.html")

@app.route("/create-post", methods=["GET","POST"])
def create_post():
    if request.method == "POST":
        author = request.form.get("author")
        content = request.form.get("content")

        if not author or not content:
            return render_template("create_post.html",error="Missing Author or Content")

        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ?",(author,)).fetchone()
        if not user:
            return render_template("create_post.html",error="Author Not Found")        
        
        db.execute("INSERT INTO posts (author,content) VALUES (?,?)",(author,content))
        db.commit()
        return redirect(url_for("home"))
    
    return render_template("create_post.html")


@app.route("/update-post", methods=["GET","POST"])
def update_post():
    if request.method == "POST":
        if request.method == "POST":
            method_override = request.form.get("_method")
            if method_override == "PUT":
                post_id = request.form.get("id")
                new_content = request.form.get("new_content")
         
                if not post_id or not new_content:
                    return render_template("update_post.html",error="Missing Post Id or Content")

                db = get_db()
                post = db.execute("SELECT * FROM posts WHERE id = ?",(post_id,)).fetchone()
                if not post:
                    return render_template("update_post.html",error="Post Not Found")
                
                db.execute("UPDATE posts SET content = ? WHERE id = ?",(new_content,post_id))
                db.commit()
                return redirect(url_for("home"))
    return render_template("update_post.html")
    



@app.route("/remove-post", methods=["GET","POST"])
def remove_post():
    if request.method == "POST":
        method_override = request.form.get("_method")
        if method_override == "DELETE":
            post_id = request.form.get("id")

            if not post_id:
                return render_template("remove_post.html", error="Missing post ID")

            
            db = get_db()
            post  = db.execute("SELECT * FROM posts WHERE id = ?",(post_id,)).fetchone()
            if not post:
                return render_template("remove_post.html", error="Post not found")
            
            db.execute("DELETE FROM posts WHERE id = ?",(post_id))
            db.commit()
            return redirect(url_for('home'))


    return render_template("remove_post.html")



if __name__ == "__main__":
    app.run(debug=True)
 
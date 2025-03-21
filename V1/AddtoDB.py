# Authors: Abby, Eion, and Brady
from flask import Flask, render_template, request, jsonify
import sqlite3
import os
import urllib.parse

app = Flask(__name__, template_folder='templates')

# Ensure templates directory exists
if not os.path.exists('templates'):
    os.makedirs('templates')

# Create a default layout.html file if it doesn't exist
layout_template_path = os.path.join('templates', 'layout.html')
if not os.path.exists(layout_template_path):
    with open(layout_template_path, 'w') as f:
        f.write("""<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <title>{% block title %}{% endblock %}</title>
        <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='site.css')}}" />
    </head>
    <body>
        <div class="navbar">
            <a href="{{ url_for('home') }}" class="navbar-brand">Home</a>
            <a href="{{ url_for('register') }}" class="navbar-item">Register</a>
            <a href="{{ url_for('users') }}" class="navbar-item">Add Users</a>
            <a href="{{ url_for('addpin') }}" class="navbar-item">Add Pin</a>
            <a href="{{ url_for('addboard') }}" class="navbar-item">Create Board</a>
        </div>
        <div class="body-content">
            {% block content %}
            {% endblock %}
            <hr/>
            <footer>
                <p>Pinspire</p>
            </footer>
        </div>
    </body>
</html>""")

# Create a default home.html file if it doesn't exist
home_template_path = os.path.join('templates', 'home.html')
if not os.path.exists(home_template_path):
    with open(home_template_path, 'w') as f:
        f.write("""{% extends 'layout.html' %}
{% block title %}Home{% endblock %}
{% block content %}
<h1>Welcome to Pinspire add to db!</h1>
{% endblock %}""")

# Home Page 
@app.route("/")
def home():
    return render_template("home.html")

#  register a new user
@app.route("/register")
def register():
    return render_template("register.html")

# add a new user to the database
@app.route("/adduser", methods=['POST'])
def adduser():
    if request.method == 'POST':
        try:
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            email = request.form['email']
            username = request.form['username']

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO user (firstname, lastname, email, username) VALUES (?, ?, ?, ?)",
                            (firstname, lastname, email, username))
                con.commit()
                msg = "User successfully registered"
        except:
            con.rollback()
            msg = "Error in registration"
        finally:
            con.close()
            return render_template('result.html', msg=msg)

# display all users
@app.route('/users')
def users():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM user")
    rows = cur.fetchall()
    con.close()
    return render_template("users.html", rows=rows)

# Add a new pin
@app.route("/addpin")
def addpin():
    return render_template("addpin.html")

@app.route("/insertpin", methods=['POST'])
def insertpin():
    if request.method == 'POST':
        try:
            image = request.form['image']
            title = request.form['title']
            description = request.form['description']

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO pins (image, title, description) VALUES (?, ?, ?)",
                            (image, title, description))
                con.commit()
                msg = "Pin successfully added"
        except:
            con.rollback()
            msg = "Error in adding pin"
        finally:
            con.close()
            return render_template('result.html', msg=msg)

# Create a board
@app.route("/addboard")
def addboard():
    return render_template("addboard.html")

@app.route("/insertboard", methods=['POST'])
def insertboard():
    if request.method == 'POST':
        try:
            image = urllib.parse.quote(request.form['cover_image'])
            title = request.form['title']

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO board (cover_image, title) VALUES (?, ?)",
                            (image, title))
                con.commit()
                msg = "Board successfully added"
        except:
            con.rollback()
            msg = "Error in adding Board"
        finally:
            con.close()
            return render_template('result.html', msg=msg)

        
# Add a comment
@app.route("/addcomment", methods=['POST'])
def addcomment():
    if request.method == 'POST':
        try:
            user_id = request.form['user_id']
            pin_id = request.form['pin_id']
            comment_text = request.form['comment_text']

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO comments (user_id, pin_id, comment_text) VALUES (?, ?, ?)",
                            (user_id, pin_id, comment_text))
                con.commit()
                msg = "Comment successfully added"
        except:
            con.rollback()
            msg = "Error in adding comment"
        finally:
            con.close()
            return render_template('result.html', msg=msg)

# Route to associate a pin with a board
@app.route("/addboardpin", methods=['POST'])
def addboardpin():
    if request.method == 'POST':
        try:
            board_id = request.form['board_id']
            pin_id = request.form['pin_id']

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO boardpins (board_id, pin_id) VALUES (?, ?)",
                            (board_id, pin_id))
                con.commit()
                msg = "Pin successfully added to board"
        except:
            con.rollback()
            msg = "Error in adding pin to board"
        finally:
            con.close()
            return render_template('result.html', msg=msg)

# Get available tables
def get_tables():
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cur.fetchall()]
    return tables

@app.route("/tables")
def tables():
    return jsonify(get_tables())

# Get data from a selected table
@app.route("/get_table_data", methods=['POST'])
def get_table_data():
    table_name = request.form['table_name']
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM {table_name} LIMIT 30")
        rows = cur.fetchall()
        columns = [description[0] for description in cur.description]
    return jsonify({"columns": columns, "rows": rows})

@app.route("/display_tables")
def display_tables():
    return render_template("display_tables.html")


if __name__ == "__main__":
    app.run(debug=True)
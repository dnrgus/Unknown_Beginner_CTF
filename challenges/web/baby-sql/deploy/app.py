import os
import sqlite3

from flask import Flask, request


app = Flask(__name__)
FLAG = os.environ.get("FLAG", "UNKNOWN{baby_sqli_login_bypass}")


def init_db():
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.execute("CREATE TABLE users (username TEXT, password TEXT)")
    conn.execute("INSERT INTO users VALUES ('admin', 'not-the-password')")
    conn.commit()
    return conn


DB = init_db()


@app.route("/", methods=["GET", "POST"])
def index():
    message = "Login as admin."
    query = ""
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        query = (
            "SELECT username FROM users "
            f"WHERE username = '{username}' AND password = '{password}'"
        )
        try:
            row = DB.execute(query).fetchone()
            if row:
                message = f"Welcome {row[0]}. Flag: {FLAG}"
            else:
                message = "Invalid username or password."
        except sqlite3.Error as exc:
            message = f"SQL error: {exc}"

    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Baby SQL</title>
    <style>
      body {{ background:#070b12; color:#eef6ff; font-family:system-ui,sans-serif; padding:4rem; }}
      main {{ max-width:720px; margin:auto; }}
      input {{ display:block; margin:.6rem 0; padding:.6rem; width:100%; max-width:360px; }}
      button {{ padding:.6rem 1rem; }}
      code {{ color:#67e8f9; white-space:pre-wrap; }}
    </style>
  </head>
  <body>
    <main>
      <h1>Baby SQL</h1>
      <p>{message}</p>
      <form method="post">
        <input name="username" placeholder="username">
        <input name="password" placeholder="password">
        <button type="submit">Login</button>
      </form>
      <p>Debug query:</p>
      <code>{query}</code>
    </main>
  </body>
</html>"""

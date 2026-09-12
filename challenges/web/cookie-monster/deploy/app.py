import os

from flask import Flask, make_response, request


app = Flask(__name__)
FLAG = os.environ.get("FLAG", "UNKNOWN{cookies_are_client_side}")


@app.get("/")
def index():
    role = request.cookies.get("role")
    if role is None:
        role = "guest"
    body = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Cookie Monster</title>
    <style>
      body {{ background:#070b12; color:#eef6ff; font-family:system-ui,sans-serif; padding:4rem; }}
      main {{ max-width:720px; margin:auto; }}
      a {{ color:#67e8f9; }}
    </style>
  </head>
  <body>
    <main>
      <h1>Cookie Monster</h1>
      <p>Your current role is <strong>{role}</strong>.</p>
      <p><a href="/admin">Open admin panel</a></p>
    </main>
  </body>
</html>"""
    response = make_response(body)
    if request.cookies.get("role") is None:
        response.set_cookie("role", "guest", httponly=False, samesite="Lax")
    return response


@app.get("/admin")
def admin():
    role = request.cookies.get("role", "guest")
    if role == "admin":
        return f"Welcome admin. Flag: {FLAG}\n"
    return "Access denied. Admin role required.\n", 403

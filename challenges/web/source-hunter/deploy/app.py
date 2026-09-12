import os

from flask import Flask, Response


app = Flask(__name__)
FLAG = os.environ.get("FLAG", "UNKNOWN{view_source_is_a_superpower}")
SECRET_PATH = "/debug-source-map-7f3a"


@app.get("/")
def index():
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Source Hunter</title>
    <!-- TODO: remove debug route before launch: {SECRET_PATH} -->
    <style>
      body {{ background:#070b12; color:#eef6ff; font-family:system-ui,sans-serif; padding:4rem; }}
      main {{ max-width:720px; margin:auto; }}
      code {{ color:#67e8f9; }}
    </style>
  </head>
  <body>
    <main>
      <h1>Source Hunter</h1>
      <p>The flag is not printed on this page.</p>
      <p>Sometimes the browser already has the clue. Inspect carefully.</p>
    </main>
  </body>
</html>"""


@app.get(SECRET_PATH)
def debug_source_map():
    return Response(f"flag={FLAG}\n", mimetype="text/plain")

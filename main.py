from flask import Flask, render_template, Markup, redirect
import os
import subprocess
import json

app = Flask(__name__)
basedir = "E:\\kalashnikov\\notes"
home = "home"

@app.route("/")
def index():
    return redirect("/{}".format(home))

@app.route("/<title>")
def showpage(title):
    filename = title + ".md"
    path_to_file = os.path.join(basedir, filename)
    html_data = subprocess.run([
        "pandoc", path_to_file, "--mathjax"], stdout=subprocess.PIPE
        ).stdout.decode("utf-8")

    return render_template("index.html",
            convertedmd=Markup(html_data), title=title)

if __name__ == "__main__":
    app.run(debug=True)

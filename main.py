from flask import Flask, render_template, Markup, redirect
import os
import subprocess
import json
import livereload

app = Flask(__name__)
config = json.loads(open("config.json", "r").read())

@app.route("/")
def index():
    return redirect("/{}".format(config["home"]))

@app.route("/<path:subpath>.md")
def showpage(subpath):
    path_to_file = os.path.join(config["basedir"], subpath + ".md")
    html_data = subprocess.run([
        "pandoc", path_to_file, "--mathjax"], stdout=subprocess.PIPE
        ).stdout.decode("utf-8")

    return render_template("index.html",
            convertedmd=Markup(html_data), title=subpath)

@app.route("/path/<path:subpath>")
def showpath(subpath):
    path = ""
    for x in subpath.split("/"):
        path = os.path.join(path, x)
    return path


if __name__ == "__main__":
    reloadserver = livereload.Server(app.wsgi_app)
    reloadserver.watch(os.path.join(config["basedir"], "*.md"))
    reloadserver.serve()

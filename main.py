from flask import Flask, Markup, redirect, send_from_directory
import os
import json
import livereload
import pypandoc

config = json.loads(open("config.json", "r").read())
app = Flask(__name__)

@app.route("/")
def index():
    return redirect("/{}".format(config["home"]))

@app.route("/<path:subpath>.md")
def showpage(subpath):
    abs_path = os.path.join(config["basedir"], subpath + ".md")
    html_data = pypandoc.convert_file(abs_path, to="html", extra_args=["-s",
        "--mathjax", "-c", "static/latex-css/style.css",
        "--filter", "pandoc-plot", "-M",
        "plot-configuration={}".format(config["plot-config"]),
        #"directory=\"{}\"".format(config["plots"])])
        ])
    return html_data

if __name__ == "__main__":
    reloadserver = livereload.Server(app.wsgi_app)
    reloadserver.watch(os.path.join(config["basedir"], "*.md"))
    reloadserver.serve(host=config["host"], port=config["port"], debug=True)

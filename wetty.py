from flask import Flask, render_template, request

wetty = Flask(__name__)


@wetty.route("/")
def hello_world():
    return render_template("search.html")

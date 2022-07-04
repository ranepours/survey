from flask import Flask, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'
debug = DebugToolbarExtension(app)
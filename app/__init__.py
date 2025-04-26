from flask import Flask, session
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)  # Change this to a strong, random key

from app import routes  # Import routes *after* app is created

from flask import render_template, request, redirect, session, flash, url_for
from flask_app import app

@app.route('/exercise/ai')
def chatbot():
    return render_template('chatBot.html')
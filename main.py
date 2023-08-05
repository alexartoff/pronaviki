from flask import Flask, render_template
from flask import request, flash, redirect, url_for
import os
from dotenv import load_dotenv, find_dotenv
from datetime import datetime


import db


load_dotenv(find_dotenv())
app = Flask(__name__, subdomain_matching=True)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SERVER_NAME'] = os.environ.get('SERVER_NAME')
subdomain = os.environ.get('SUBDOMAIN')


@app.route('/', subdomain=subdomain)
# @app.route('/')
async def main_page():
    db_data = await db.get_from_pg()
    date = datetime.now()
    return render_template('index.html', celebs=db_data, date=date)


@app.route('/form', methods=('GET', 'POST'), subdomain=subdomain)
# @app.route('/form', methods=('GET', 'POST'))
async def form():
    if request.method == 'POST':
        user_name = request.form['user_name']
        user_question = request.form['user_question']
        user_email = request.form['user_email']
        if not user_name or not user_question or not user_email:
            flash('Fill the form!', category='danger')
        else:
            if await db.add_question(user_name, user_question, user_email):
                flash('data send', category='success')
                return redirect(url_for('main_page'))
            else:
                flash('Something wrong in db...', category='danger')
    return render_template('form.html')

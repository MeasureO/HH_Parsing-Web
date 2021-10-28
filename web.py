from flask import Flask, render_template, request, redirect, send_file
from hh_parser import get_jobs
from exp_csv import save_to_csv

app = Flask(__name__)
app.debug = True

db = {}

@app.route('/')
def home():
  return render_template('home.html')
# @app.route('/<username>')
# def contact_page(username):
#     return f'Hi, {username}!'
@app.route('/report')
def report():
    keyword = request.args.get('keyword')
    if keyword is not None:
        keyword = keyword.lower()
        getDb = db.get(keyword)
        if getDb:
            jobs = getDb
        else:
            jobs = get_jobs(keyword)
            db[keyword] = jobs
        # print(jobs)
    else:
        return redirect('/')
    return render_template('report.html', searchBy=keyword, resultsNumber=len(jobs), jobs = jobs, thanks='Спасибо!')

@app.route('/export')
def export():
    try:
        keyword = request.args.get('keyword')
        if not keyword:
            raise Exception()
        keyword = keyword.lower()
        jobs = db.get(keyword)
        if not jobs:
            raise Exception()
        save_to_csv(jobs)
        return send_file('jobs.csv')
    except:
        return redirect('/')
app.run(host='0.0.0.0')

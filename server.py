from flask import Flask, render_template, request, Response, send_from_directory, make_response
from flask.ext.httpauth import HTTPDigestAuth
from datetime import datetime, date
import json
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'kidnetics'
client = MongoClient()
db = client.kidnetics
auth = HTTPDigestAuth()

users = {
	"employee": "abc123"
}

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

@app.route('/', methods=['GET', 'POST'])
@auth.login_required
def root():
	if request.method=='POST':
			form=dict(request.form)
			form={i:j[0] for i,j in form.items() }
			form['children']=[dict(zip(['Name', 'DOB'], i.split(','))) for i in form['children'].split(";")]
			form['date']=datetime.combine(date.today(), datetime.min.time())
			db.waivers.insert(form)
	return render_template("index.html")

@app.route('/waivers')
@auth.login_required
def waivers():
	return render_template("waivers.html", waivers=db.waivers.find())

@app.route('/<filename>.json')
@auth.login_required
def waiver(filename):
	name, date_added=filename.split(".")
	name, date_added=name.replace('_', ' '), datetime.combine(datetime.strptime(date_added, "%d-%m-%y"), datetime.min.time())
	waiver=db.waivers.find({"name": name, "date": date_added})[0]
	waiver['date']=str(date)
	del waiver['_id']
	response=make_response(json.dumps(waiver, sort_keys=True, indent=4, separators=(',', ': ')))
	response.headers['Content-Type'] = 'application/json'
	response.headers['Content-Disposition'] = 'attachment; filename=%s.json' % filename
	return response

@app.route('/<path:filename>')  
@auth.login_required
def send_file(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
	app.run(debug=True)
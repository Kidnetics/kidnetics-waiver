from flask import Flask, render_template, request, Response
from flask.ext.httpauth import HTTPDigestAuth
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import os

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'kidnetics'
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
		with open("static\\waivers\\"+request.form['name'].replace(' ', '.')+'_'+datetime.now().strftime("%y.%m.%d")+'.json', 'w') as report:
			form=dict(request.form)
			form={i:j[0] for i,j in form.items() }
			form['children']=[dict(zip(['Name', 'DOB'], i.split(','))) for i in form['children'].split(";")]
			report.write(json.dumps(form, sort_keys=True, indent=4, separators=(',', ': ')))
	return render_template("index.html")

@app.route('/<path>')
def other(path):
	return app.send_static_file(path)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
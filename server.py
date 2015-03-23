from flask import Flask, render_template, request, Response
from flask.ext.httpauth import HTTPDigestAuth

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
		print(request.form)
	return render_template("index.html")

@app.route('/<path>')
def other(path):
	return app.send_static_file(path)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
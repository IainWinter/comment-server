from flask import Flask, request, jsonify
from logic import *
from data import db_close

app = Flask(__name__)

# This gets ran everytime the file is saved, so all queries need to INSERT OR IGNORE
with app.app_context():
	init_tables()
	create_subject("epa-algorithm", "What is the answer to life, the universe and everything?", "42")

def send_json(obj):
	response = jsonify(obj)
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response

def get_ip(request) -> str:
	# for reverse proxy pass
	return request.headers.get('X-Real-IP', request.remote_addr)

@app.route("/comment-get/<subject>")
def comment_get(subject):
	ip = get_ip(request)
	return send_json(get_comments_for_subject(ip, subject))

@app.route("/comment-post/<subject>/<parent>")
def comment_post(subject, parent):
	ip = get_ip(request)
	test = request.args.get('test')
	name = request.args.get('name')
	content = request.args.get('content')

	return send_json(try_post_comment(ip, subject, test, parent, name, content))

@app.route("/comment-edit/<edit_key>")
def comment_edit(edit_key):
	ip = get_ip(request)
	name = request.args.get('name')
	content = request.args.get('name')

	return send_json(try_edit_comment(ip, edit_key, name, content))

@app.route("/comment-delete/<edit_key>")
def comment_delete(edit_key):
	ip = get_ip(request)
	return send_json(try_delete_comment(ip, edit_key))

@app.route("/comment-subjects")
def comment_subjects():
	return send_json(get_all_subjects())

@app.teardown_appcontext
def close_connection(exception):
	db_close()

# Only if server is running through cli
if __name__ == '__main__':
	print("Starting server...")
	app.run(debug=True, use_reloader=False)
from flask import Flask, request, jsonify
from logic import *
from data import init_tables, create_subject, db_close

app = Flask(__name__)

# This gets ran every time the file is saved, so all queries need to INSERT OR IGNORE
with app.app_context():
	init_tables()
	create_subject("epa-algorithm", "Which direction of normal was calculated in EPA.js?", "right")
	create_subject("gjk-algorithm", "What is the 3D case of the GJK algorithm called?", "tetrahedron")
	create_subject("falling-sand", "What is the R, G, B color of _SAND in sketch.pde?", "255,150,50")
	create_subject("falling-sand-worlds", "What is the hex number used in pair_hash.h?", "0x1f1f1f1f")
	create_subject("physics-engine", "What is the name of the class which fixes stuttery movement?", "physicssmoothstepsystem")
	create_subject("another-way", "What was the file name used for the example code?", "typeerasurecopy.h")
	create_subject("support", "What is the domain of this website?", "winter.dev")

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

	if not test or not name or not content:
		return send_json({"error": "invalid"})

	return send_json(try_post_comment(ip, subject, test, parent, name, content))

@app.route("/comment-edit/<edit_key>")
def comment_edit(edit_key):
	ip = get_ip(request)
	name = request.args.get('name')
	content = request.args.get('content')

	if not name or not content:
		return send_json({"error": "invalid"})

	return send_json(try_edit_comment(ip, edit_key, name, content))

@app.route("/comment-delete/<edit_key>")
def comment_delete(edit_key):
	ip = get_ip(request)
	return send_json(try_delete_comment(ip, edit_key))

@app.errorhandler(404)
def page_not_found(e):
	with open('./log.txt', 'a') as file:
		file.write(request.url + '\n')
	return "404"

@app.teardown_appcontext
def close_connection(exception):
	db_close()

# Only if server is running through cli
if __name__ == '__main__':
	print("Starting server...")
	app.run(debug=True, use_reloader=False, port=80)
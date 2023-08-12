from flask import Flask, request, jsonify
from logic import *
from data import db_close

app = Flask(__name__)

# This gets ran everytime the file is saved, so all queries need to INSERT OR IGNORE
with app.app_context():
	init_tables()
	create_subject("epa-algorithm", "Which direction of normal was calculated in EPA.js? (right or left)", "right")
	create_subject("gjk-algorithm", "What is the 3D case of the GJK algorithm called?", "tetrahedron")
	create_subject("falling-sand", "What is the RGB color of _SAND in sketch.pde? (R, G, B)", "255,150,50")
	create_subject("falling-sand-worlds", "What is the final typename, without namespace, of the map used for m_chunkLookup?", "concurrent_unordered_map")
	create_subject("physics-engine", "What is the name of the class which fixes stuttery movment?", "physicssmoothstepsystem")
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
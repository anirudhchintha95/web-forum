"""
This is the main file for the application.
"""
from flask import Flask, g, request, abort, make_response, jsonify
from bson.objectid import ObjectId
from db import DB
from models import User, Post

app = Flask(__name__)

@app.before_request
def get_db():
    """
    Get the database object and assign it to globals
    """
    if "db" not in g:
        db_instance = DB("mongodb://localhost:27017", "test")
        db_instance.connect()
        g.db = db_instance


@app.errorhandler(404)
def page_not_found(e):
    """
    Handle 404 errors
    """
    return make_response(jsonify({"err": "Page not found"}), 404)


@app.errorhandler(405)
def method_not_defined(e):
    """
    Handle 405 errors
    """
    return make_response(jsonify({"err": "Method not defined"}), 405)


@app.errorhandler(400)
def handle_400(e):
    """
    Handle 400 errors
    """
    return make_response(jsonify({"error": e.description}), 400)


@app.route("/posts", methods=["GET", "POST"])
def posts():
    """
    Get all posts or create a new post
    """
    if request.method == "GET":
        postsList = Post.objects()
        return [item.to_response for item in postsList]
    elif request.method == "POST":
        # Implement create post here
        pass
    else:
        abort(404, "Method not allowed")

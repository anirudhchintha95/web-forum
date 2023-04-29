from flask import Blueprint, request, abort, g
from application.controllers.posts import (
    create_post,
    get_post_by_counter_id,
    delete_post,
    get_posts
)

bp = Blueprint("post", __name__, url_prefix="/post")


@bp.route("/", methods=["GET", "POST"])
def create_post_route():
    """
    Create a post which is not associated with any user
    """
    if request.method == "POST":
        try:
            if not request.json.get("msg"):
                raise Exception("msg is required")

            post = create_post(g.get("current_user"), request.json["msg"])
            post = post.to_response()
            return post
        except Exception as e:
            abort(400, str(e))
    elif request.method == "GET":
        return get_posts()
    else:
        abort(404, "Method not allowed")


@bp.route("/<post_counter_id>", methods=["GET"])
def get_post_route(post_counter_id):
    """
    Get a post by id
    """
    if request.method == "GET":
        try:
            post = get_post_by_counter_id(g.get("current_user"), post_counter_id)
            return post.to_response(True)
        except Exception as e:
            abort(400, str(e))
    else:
        abort(404, "Method not allowed")


@bp.route("/<post_counter_id>/delete/<id>", methods=["DELETE"])
def delete_post_route(post_counter_id, id):
    """
    Delete a post
    """
    if request.method == "DELETE":
        try:
            post = delete_post(g.get("current_user"), post_counter_id, id)
            return post.to_response()
        except Exception as e:
            abort(400, str(e))
    else:
        abort(404, "Method not allowed")

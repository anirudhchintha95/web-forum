from flask import Blueprint, request, abort, g
from application.controllers.posts import (
    create_post,
    get_post_by_counter_id,
    delete_post,
    get_posts,
    get_posts_search,
)
from application.models.errors import NotFoundError, UnauthorizedError

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
        abort(405, "Method not allowed")


@bp.route("/<int:post_counter_id>", methods=["GET"])
def get_post_route(post_counter_id):
    """
    Get a post by id
    """
    if request.method == "GET":
        try:
            post = get_post_by_counter_id(g.get("current_user"), post_counter_id)
            return post.to_response(True)
        except NotFoundError as e:
            abort(404, str(e))
        except Exception as e:
            abort(400, str(e))
    else:
        abort(405, "Method not allowed")


@bp.route("/<post_counter_id>/delete/<id>", methods=["DELETE"])
def delete_post_route(post_counter_id, id):
    """
    Delete a post
    """
    if request.method == "DELETE":
        try:
            post = delete_post(g.get("current_user"), post_counter_id, id)
            return post.to_response()
        except NotFoundError as e:
            abort(404, str(e))
        except UnauthorizedError as e:
            abort(403, str(e))
        except Exception as e:
            abort(400, str(e))
    else:
        abort(405, "Method not allowed")


@bp.route("/query/search", methods=["GET"])
def search_post_route():
    """
    Search a post
    """
    search = request.args.get("search")
    if request.method == "GET":
        try:
            posts = get_posts_search(search)
            return posts
        except Exception as e:
            abort(400, str(e))
    else:
        abort(404, "Method not allowed")

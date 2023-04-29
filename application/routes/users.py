from flask import Blueprint, request, abort
import application.controllers.users as users_controller

bp = Blueprint("users", __name__, url_prefix="/users")


@bp.route("/create", methods=["POST"])
def register():
    """
    Register a user
    """
    if request.method == "POST":
        try:
            if not request.json.get("username") or not request.json.get("password"):
                raise Exception("Username and password are required")

            user = users_controller.create_user(
                request.json["username"], request.json["password"]
            )
            return user.to_response()
        except Exception as e:
            abort(400, str(e))
    else:
        abort(404, "Method not allowed")

@bp.route("/<user_key>/posts/create", methods=["POST"])
def create_post_user_route(user_key):
    """
    Creating a post for the user
    """
    if request.method == "POST":
        try:
            if not request.json.get("msg"):
                raise Exception("msg is required")

            user = users_controller.get_user_by_key(user_key)
            post = users_controller.create_post(user, request.json["msg"])
            print("post", post)
            return post.to_response()
        except Exception as e:
            abort(400, str(e))
    else:
        abort(404, "Method not allowed")

@bp.route("/<user_counter_id>/posts", methods=["GET"])
def get_posts_user_route(user_counter_id):
    """
    Get all posts for the user
    """
    if request.method == "GET":
        try:
            user = users_controller.get_user_by_counterId(user_counter_id)
            posts = users_controller.get_posts(user)
            return posts
        except Exception as e:
            abort(400, str(e))
    else:
        abort(404, "Method not allowed")

@bp.route("/<user_counter_id>/posts/<post_counter_id>/delete/<post_key>", methods=["DELETE"])
def delete_post_user_route(user_counter_id, post_counter_id, post_key):
    """
    Delete a post of a user
    """
    if request.method == "DELETE":
        try:
            user = users_controller.get_user_by_counterId(user_counter_id)
            post = users_controller.delete_post(user, post_counter_id, post_key)
            return post.to_response()
        except Exception as e:
            abort(400, str(e))
    else:
        abort(404, "Method not allowed")

@bp.route("/<user_counter_id>/posts/<other_user_counter_id>", methods=["GET"])
def get_other_user_posts(user_counter_id, other_user_counter_id):
    """
    Get all posts for the user
    """
    if request.method == "GET":
        try:
            user = users_controller.get_user_by_counterId(user_counter_id)
            otheruser= users_controller.get_user_by_counterId(other_user_counter_id)
            posts = users_controller.get_posts(otheruser)
            return posts
        except Exception as e:
            abort(400, str(e))
    else:
        abort(404, "Method not allowed")
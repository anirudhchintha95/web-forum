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




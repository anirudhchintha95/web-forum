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
            validate_fields = ["username", "password", "firstname"]
            for field in validate_fields:
                if not request.json.get(field):
                    raise Exception(f"{field} is required")

            user = users_controller.create_user(
                request.json["username"], request.json["password"], request.json["firstname"]
            )
            return user.to_response()
        except Exception as e:
            abort(400, str(e))
    else:
        abort(404, "Method not allowed")

# Get a user by user key
@bp.route("/<user_key>", methods=["GET"])
def get_user_route(user_key):
    """
    Get a user by counterId
    """
    if request.method == "GET":
        try:
            user = users_controller.get_user_by_key(user_key)
            return user.to_response()
        except Exception as e:
            abort(400, str(e))
    else:
        abort(404, "User not found")

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

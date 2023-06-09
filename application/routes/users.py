from flask import Blueprint, request, abort, g, jsonify
import application.controllers.users as users_controller
from application.models.errors import NotFoundError

bp = Blueprint("users", __name__, url_prefix="/users")


@bp.route("/create", methods=["POST"])
def register():
    """
    Register a user
    """
    if request.method == "POST":
        try:
            params = {"username": "", "password": "", "firstname": ""}
            for field in params:
                params[field] = request.json.get(field)
                if params[field] is None:
                    raise Exception(f"{field} is required")
                if not isinstance(params[field], str):
                    raise Exception(f"{field} value should be string")
                params[field] = params[field].strip()
                if params[field] == "":
                    raise Exception(f"{field} cannot be empty")

            user = users_controller.create_user(
                params["username"], params["password"], params["firstname"]
            )
            return user.to_response()
        except Exception as e:
            abort(400, str(e))
    else:
        abort(404, "Method not allowed")


# Get a user by user key
@bp.route("/<int:user_counter_id>", methods=["GET"])
def get_user_route(user_counter_id):
    """
    Get a user by counterId
    """
    if request.method == "GET":
        try:
            current_user = g.get("current_user")
            if current_user is None:
                return jsonify(error="Unauthorized"), 403
            user = users_controller.get_user_by_counterId(user_counter_id)
            return user.to_response(True)
        except NotFoundError as e:
            abort(404, str(e))
        except Exception as e:
            abort(400, str(e))
    else:
        abort(404, "User not found")


# Edit a user by user counter id
@bp.route("/edit", methods=["PUT"])
def edit_user_route():
    """
    Edit a user by counterId
    """
    if request.method == "PUT":
        current_user = g.get("current_user")
        if current_user is None:
            abort(403, "Unauthorized")
        user_key = request.headers.get("user_key")
        username = request.json.get("username") or ""
        password = request.json.get("password") or ""
        firstname = request.json.get("firstname") or ""
        try:
            user = users_controller.edit_user_by_key(
                user_key, username.strip(), password.strip(), firstname.strip()
            )
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
        except NotFoundError as e:
            abort(404, str(e))
        except Exception as e:
            abort(400, str(e))
    else:
        abort(404, "Method not allowed")

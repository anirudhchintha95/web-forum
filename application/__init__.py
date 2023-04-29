from flask import Flask, g, make_response, jsonify, request
from application.config import Config
from application.db import DB
from application.controllers.users import get_user_by_key


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    @app.before_request
    def get_db():
        """
        Get the database object and assign it to globals
        """
        if "db" not in g:
            db_instance = DB(app.config.get("DB_URL"), app.config.get("DB_NAME"))
            db_instance.connect()
            g.db = db_instance
        user_key = request.headers.get("user_key")
        if user_key:
            g.current_user = get_user_by_key(user_key)


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

    from application.routes import posts_bp, users_bp

    app.register_blueprint(posts_bp)
    app.register_blueprint(users_bp)

    return app

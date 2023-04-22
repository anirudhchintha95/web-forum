from flask import Flask, g, make_response, jsonify
from application.config import Config
from application.db import DB


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

    return app
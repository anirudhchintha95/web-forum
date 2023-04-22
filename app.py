"""
This is the main file for the application.
"""

from application import create_app

app = create_app()

if __name__ == "__main__":
    app.run()

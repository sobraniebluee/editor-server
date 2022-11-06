from src import create_app
from os import environ

if __name__ == "__main__":
    app = create_app()
    app.run()

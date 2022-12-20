from src import create_app, app

if __name__ == "__main__":
    init_app = create_app()
    init_app.run(host="127.0.0.1", app=app, debug=True, port=5000)
